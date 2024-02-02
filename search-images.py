# This script accesses environment variables 
#      GH_ACCESS_TOKEN, COMPUTER_VISION_ENDPOINT, COMPUTER_VISION_SUBSCRIPTION_KEY
# see readme for details

# This script uses the following packages:
#     pip install azure-ai-vision-imageanalysis
#     pip install pillow
#     pip install PyGithub  
# *** PUT YOUR DETAILS HERE  *****

# what to search
find_text = ["Microsoft"]            # Text to find in the images.  
case_sensitive = False                    # True or False
csv_fn = "msft.csv"          # Put results in this file

# where to search
repo_name = "MicrosoftDocs/azure-docs"  # repo to search
branch = "main"
media_path = 'articles/machine-learning/v1/media'  # point to the media dir you want to search
# or here's fabric:
# repo_name = "MicrosoftDocs/fabric-docs"
# branch = "main"
# media_path = 'docs/data-science/media' 

# *** END OF SEARCH DETAILS ***

# form vars from search details above
md_fn = csv_fn.split(".")[0] + ".md"  # Put previews in markdown file
online_url = f"https://raw.githubusercontent.com/{repo_name}/{branch}/" # to get raw images from the repo  

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import os
import time
import datetime
from auth import get_auth_response

# get vision tokens and the repo
endpoint, key, repo = get_auth_response(repo_name)

# Create an Image Analysis client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)


# open csv file to store results
import csv
# Write results to csv file
f = open(csv_fn, 'w+')
# write header
f.write("status,url\n")
# add previews to an md file
m = open(md_fn, 'w+')
m.write("# Previews of the found files\n") 
# initialize counts
pr = 0
found = 0
unk = 0

# Start search 
st = time.time()

print(f"===== Start Searching Files for {find_text} in {repo_name} ====")
print(str(datetime.datetime.now()))

contents = repo.get_contents(media_path)
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        img_url = online_url + file_content.path       
    
        try:
            # analyze image
            result = client.analyze(
                image_url=img_url,
                visual_features=[VisualFeatures.READ],
            )   
            # if there are results
            if result.read is not None:
                pr += 1
                # If find_text is found, add the image to the csv and md files
                if result.text is not None:
                    for line in result.read.blocks[0].lines:
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
                if os.path.splitext(file_content.path)[1] != '.png': # dont care about png with no text
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
print(f" Files to investigate: {unk}")
print(f" See results in {csv_fn} and {md_fn}")
print(f" Execution time: {elapsed} minutes")
