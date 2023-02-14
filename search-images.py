# This script accesses environment variables 
#      GH_ACCESS_TOKEN, COMPUTER_VISION_ENDPOINT, COMPUTER_VISION_SUBSCRIPTION_KEY
# see readme for details

# This script needs the following packages:
#     pip install --upgrade azure-cognitiveservices-vision-computervision
#     pip install pillow
#     pip install PyGithub  

# *** PUT YOUR DETAILS HERE  *****
# where to search
# Point to any media directory in MicrosoftDocs/azure-docs/
path_in_repo = 'articles/machine-learning/v1/media'    # Path to your files from MicrosoftDocs/azure-docs/
# what to search
find_text = "Data Labeling"            # Text to find in the images.  (text is case sensitive)
write_fn = "DataLabeling.csv"          # Put results in this file
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
token =  os.environ['GH_ACCESS_TOKEN']
g = Github(token)

# Authenticate with key, endpoint from environment variables (assumes you've exported these)
endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
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

# initialize counts
pr = 0
found = 0
unk = 0

# Start search 
st = time.time()

print("===== Start Searching Files for '" + find_text + "' ====")
print(str(datetime.datetime.now()))

# hard-coded to work with azure-docs.  perhaps change this to be configurable as well
repo = g.get_repo("MicrosoftDocs/azure-docs")
online_url = 'https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/'   

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
                        if (line.text.find(find_text))>= 0:
                            f.write("found, " + img_url )
                            f.write("\n")
                            found += 1
                            print("Found: " + img_url)  

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

et = time.time()
elapsed = et - st

print("==== Done Searching Files for '" + find_text + "' ====")
print(" Files processed: " + str(pr))
print(" Files containing '" + find_text + "': " + str(found))
print(" Files to investigate (.svg & .gif): " + str(unk))
print(" See results in " + write_fn)
print(" Execution time: ", elapsed, " seconds")