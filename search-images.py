# This script accesses environment variables 
#      GH_ACCESS_TOKEN, COMPUTER_VISION_ENDPOINT, COMPUTER_VISION_SUBSCRIPTION_KEY
# see readme for details

# This script needs the following packages:
#     pip install --upgrade azure-cognitiveservices-vision-computervision
#     pip install pillow
#     pip install PyGithub  

# *** PUT YOUR DETAILS HERE  *****
# where to search

# what to search
find_text = ["Power BI dataset"]            # Text to find in the images.  
case_sensitive = False                    # True or False
write_fn = "pbi-dataset.csv"          # Put results in this file
write_md = "pbi-dataset.md"

# configurer repo
# repo_name = "MicrosoftDocs/azure-docs"  # repo to search
# online_url = 'https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/'   
# path_in_repo = 'articles/machine-learning/media'  # point to the media dir you want to search

repo_name = "MicrosoftDocs/fabric-docs"
path_in_repo = 'docs/data-science/media' 
online_url = 'https://raw.githubusercontent.com/MicrosoftDocs/fabric-docs/main/' 

# *** END OF SEARCH DETAILS ***

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import datetime
import os
from github import Github

# *** AUTHENTICATE 
# Get GH access token from environment variables (assumes you've exported this)
# try to read GH_ACCESS_TOKEN from environment variables
# if not there, tell user to set it
try:
    token = os.environ['GH_ACCESS_TOKEN']   
except:
    print("Please set GH_ACCESS_TOKEN environment variable")
    sys.exit()  

g = Github(token)
repo = g.get_repo(repo_name)

# Authenticate with key, endpoint from environment variables (assumes you've exported these)
# if not there, tell user to set it
try:    
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
except:
    print("Please set COMPUTER_VISION_ENDPOINT environment variable")
    sys.exit()

try:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
except:
    print("Please set COMPUTER_VISION_SUBSCRIPTION_KEY environment variable")
    sys.exit()
# *** End of Authenticate - you're now ready to run the script.


# connect to the endpoint
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# open csv file to store results
import csv
# Write results to csv file
f = open(write_fn, 'w+')
# write header
f.write("status, url")
f.write("\n")

m = open(write_md, 'w+')
m.write("previews of the found files") 
m.write("\n") # add previews to an md file
# initialize counts
pr = 0
found = 0
unk = 0

# Start search 
st = time.time()

print(f"===== Start Searching Files for {find_text} in {repo_name} ====")
print(str(datetime.datetime.now()))



contents = repo.get_contents(path_in_repo)
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        img_url = online_url + file_content.path

        try:
            # Call API with URL and raw response (allows you to get the operation location)
            read_response = computervision_client.read(img_url,  raw=True)

            # Get the operation location (URL with an ID at the end) from the response
            read_operation_location = read_response.headers["Operation-Location"]
            # Grab the ID from the URL
            operation_id = read_operation_location.split("/")[-1]

            # Call the "GET" API and wait for it to retrieve the results 
            while True:
                read_result = computervision_client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)
            pr += 1

            # If find_text is found, add the image to the csv file
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        for text in find_text:
                            txt_found = line.text.find(text) >= 0 if case_sensitive else line.text.lower().find(text.lower()) >= 0
                            if txt_found :
                                f.write(f"{text}: {img_url}")
                                f.write("\n")
                                m.write(f"{text}: {img_url}")
                                m.write(f"<img src='{img_url}' width=500 >")
                                m.write("\n\n")
                                found += 1
                                print(f"{text}: {img_url}")  

            '''
            END - Read File - remote
            '''
        except:
            if os.path.splitext(file_content.path)[1] != '.png':
                f.write("unknown, " + img_url)
                f.write("\n")
                unk += 1
                print("Unknown: " + img_url)
                
f.close()
m.close()

et = time.time()
elapsed = (et - st)/60

print(f"===== Done searching files for {find_text} in {repo_name} ====")
print(f" Files processed:  {pr}")
print(f" Files containing {find_text}: {found}")
print(f" Files to investigate (.svg & .gif): {unk}")
print(f" See results in {write_fn}")
print(f" Execution time: {elapsed} minutes")