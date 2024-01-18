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

# configure repo
repo_name = "MicrosoftDocs/azure-docs"  # repo to search
online_url = 'https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/'   
path_in_repo = 'articles/machine-learning/v1/media'  # point to the media dir you want to search

# repo_name = "MicrosoftDocs/fabric-docs"
# path_in_repo = 'docs/data-science/media' 
# online_url = 'https://raw.githubusercontent.com/MicrosoftDocs/fabric-docs/main/' 

# *** END OF SEARCH DETAILS ***

import os
import azure.ai.vision as sdk

import os
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

service_options = sdk.VisionServiceOptions(endpoint, subscription_key)
analysis_options = sdk.ImageAnalysisOptions()
analysis_options.features = (
    sdk.ImageAnalysisFeature.TEXT
)
analysis_options.language = "en"


# open csv file to store results
import csv
# Write results to csv file
f = open(write_fn, 'w+')
# write header
f.write("status, url")
f.write("\n")
# add previews to an md file
m = open(write_md, 'w+')
m.write("# Previews of the found files\n") 
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
        vision_source = sdk.VisionSource(url=img_url)
        image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)
        result = image_analyzer.analyze()
    
        # If find_text is found, add the image to the csv file
        try:
            if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
                pr += 1
                if result.text is not None:
                    for line in result.text.lines:
                        for text in find_text:
                            txt_found = line.text.find(text) >= 0 if case_sensitive else line.text.lower().find(text.lower()) >= 0
                            if txt_found :
                                f.write(f"{text}: {img_url}")
                                f.write("\n")
                                m.write(f"{text}: {img_url}")
                                m.write(f"<img src='{img_url}' width=500 >")
                                m.write("\n\n")
                                found += 1 
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
print(f" Files to investigate (.gif): {unk}")
print(f" See results in {write_fn}")
print(f" Execution time: {elapsed} minutes")