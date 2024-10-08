# # see https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40?tabs=visual-studio%2Clinux&pivots=programming-language-python

import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential


# Set the values of your computer vision endpoint and computer vision key
# as environment variables:
try:
    endpoint = os.environ["COMPUTER_VISION_ENDPOINT"]
    key = os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT'")
    print("Set it before running this sample.")
    exit()
print(endpoint)
# endpoint = "https://sdg-search-images-bami.cognitiveservices.azure.com/"
# cred = DefaultAzureCredential(exclude_interactive_browser_credential=False)
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)
# Create an Image Analysis client
# client = ImageAnalysisClient(endpoint=endpoint, credential=cred)

# Get a text for this image. This will be a synchronously (blocking) call.
result = client.analyze_from_url(
    image_url="https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png",
    visual_features=[VisualFeatures.READ],
)
print("Image analysis results:")

# Print text (OCR) analysis results to the console
print(" Read:")
if result.read is not None:
    for line in result.read.blocks[0].lines:
        print(f"   Line: '{line.text}'")
