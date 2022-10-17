# search-images: Find text inside images

![search-images](media/search-for-text.png)

How to solve a (not so theoretical) problem:

> I'm documenting a UI, and a term in the UI has changed.  How do I find all the images that use this term?  I have 100s (or even 1000s) of images, and I don't want to have to open each one!

The **search-images.py** Python script searches for text inside images!

## Prerequisite

* Run [Quickstart: Optical character recognition (OCR)](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/client-library?tabs=visual-studio&pivots=programming-language-python
).  

* Install the PyGithub package

    ```console
    pip install PyGithub  
    ```

* Create a [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). In step 8, set the scope to **repo**.

* Create the following environment variables:

    * GH_ACCESS_TOKEN - the token you just created from Github
    * COMPUTER_VISION_ENDPOINT - the endpoint you created from the OCR Quickstart
    * COMPUTER_VISION_SUBSCRIPTION_KEY - the key you created from the OCR Quickstart

## Run the script

1. Edit the file **search-image.py** and fill out the `PUT YOUR DETAILS HERE` section with your values.  This is where you say what to search for, where to search, where to write results.

1. Run **search-images.py**.
    * Go grab a coffee, go to lunch, or find something else to work on.  
    * For 600 images, the script took approximately 15 minutes to complete. Your milage may vary.

## Errors

If the file can't be processed, or if it does not contain text, you'll see `*** ERROR FOR FILE *** ` appear in the output, along with the link to the online file.  The script then proceeds to the next file.

* You can ignore .png files with this error, it means there was no text.
* You should manually inspect the .svg and .gif files.

## Future directions

* When I need it, I'll modify this to search for multiple terms, right now I'm just looking for one.
* Search is case sensitive.  Modify if necessary to make it case insensitive/
* You could adapt the script to process local files, following the example from [OCR: Read File using the Read API, extract text - local](https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/ComputerVisionQuickstart.py#L99). Note the sleep time in that loop is 10 times larger than for online files. 
