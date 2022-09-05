from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

# *** PUT YOUR DETAILS HERE  *****
find_text = "Datastores"                # Text to find in the images
write_fn = "v1-datastores.csv"             # Put results in this file
local_repo = 'C:/GitPrivate/azure-docs-pr'  # Where your local rep is located
repo_url = 'https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main'    # Replace last part with your repo name & branch
path_in_repo = '/articles/machine-learning/v1/media'    # Path to your files from root of your repo
# *** End of details section ***

# *** AUTHENTICATE - use one of these two methods, comment out the other
# Authenticate with key, endpoint from environment variables (assumes you've exported these)
import os
endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']

# Or uncomment and fill in your values endpoint and key from the Azure portal. 
'''
# Authenticate with key, endpoint from Cognitive Services
subscription_key = "<ADD-YOUR-KEY>"
endpoint = "<ADD-YOUR-ENDPOINT>"
'''
# *** End of Authenticate - you're now read to run the script.
# form paths for search
img_path = local_repo + path_in_repo
url_path = repo_url + path_in_repo

# connect to the endpoint
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# open csv file to store results
import csv
# Write results to csv file
f = open(write_fn, 'w+')
writer = csv.writer(f)

# initialize counts
pr = 0
found = 0

import datetime
now = datetime.datetime.now()

# Start search 
print(str(now))
print("===== Start Searching Files for '" + find_text + "' ====")

import os
# find the file names from the local repo.
for path,dirs,files in os.walk(img_path):
    for file in files: 
        image_file = os.path.join(path,file)
        # create the url for the public repo file (url works much faster than opening the local file)
        url = image_file.replace(img_path, url_path)

        try:
            # Call API with URL and raw response (allows you to get the operation location)
            read_response = computervision_client.read(url,  raw=True)

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
                            f.write(url)
                            f.write("\n")
                            found += 1
                            print("Found: " + url)  

            '''
            END - Read File - remote
            '''
        except:
            print("*** ERROR FOR FILE *** " + url)


f.close()
print("==== Done Searching Files for '" + find_text + "' ====")
print(" Files processed: " + str(pr))
print(" Files containing '" + find_text + "': " + str(found))
print(" See results in " + write_fn )
now = datetime.datetime.now()
print(str(now))