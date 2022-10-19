# from https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/client-library?tabs=visual-studio&pivots=programming-language-python
# Trying out the quickstart before I modify it for use in search-images.py

# This script needs the following packages:
# pip install --upgrade azure-cognitiveservices-vision-computervision
# pip install pillow

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

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
# *** End of Authenticate - you're now ready to run the script.

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
'''
END - Authenticate
'''

'''
OCR: Read File using the Read API, extract text - remote
This example will extract text in an image, then print results, line by line.
This API call can also extract handwriting style text (not shown).
'''
print("===== Read File - remote =====")
# Get an image with text
read_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/articles/machine-learning/media/how-to-create-labeling-projects/add-label.png"
# read_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/articles/machine-learning/media/how-to-create-attach-studio/create-schedule.png"
# Call API with URL and raw response (allows you to get the operation location)
read_response = computervision_client.read(read_image_url,  raw=True)

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

# my modification:  Print if the words "Data Labeling" appear in the image
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            if (line.text.find("Data Labeling"))>= 0:
                print("*** Found: ", line.text, "! ***")

print()
'''
END - Read File - remote
'''

print("End of Computer Vision quickstart.")