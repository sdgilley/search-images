# search-images: Find text inside images

![search-images](media/search-for-text.png)

How to solve a (not so theoretical) problem:

> I'm documenting a UI, and a term in the UI has changed.  How do I find all the images that use this term?  I have 100s (or even 1000s) of images, and I don't want to have to open each one!

This **search-images.py** Python script searches for text inside images!

**search-images.py** expects that you have a local repo that corresponds to a public online repo.  For example, your local fork of azure-docs-pr, with the online images at azure-docs.

The script uses your local directory to find the list of files to search, then processes each image from the online location to look for the search term.  

Online processing is faster than local processing.  So if the images exist online, processing them there is best.

## Prerequisite

Run [Quickstart: Optical character recognition (OCR)](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/client-library?tabs=visual-studio&pivots=programming-language-python
).  

Once you've successfully run the script from the quickstart, you'll have everything you need to run my modification of this quickstart to find images containing your search term.

## Run the script

1. Pull from your online repo to make sure you have the latest version locally.

1. Edit the file **search-images.py** and fill out the following sections:

    1. Fill out the `PUT YOUR DETAILS HERE` section with your values.  This is where you say what to search for, where to search, where to write results, and how to find the online version of the images.
    
    1. Do one of the following for the `AUTHENTICATION` method: 
        * Export  environment variables COMPUTER_VISION_ENDPOINT & COMPUTER_VISION_SUBSCRIPTION_KEY with your values to use the default method
        * To specify your own key and endpoint directly in the code, as in the quickstart, uncomment that section and add your own values. Make sure you then comment out the environment variables section

1. Finally, run **search-images.py**.
    * Go grab a coffee, go to lunch, or find something else to work on.  
    * For 600 images, the script took approximately 15 minutes to complete. Your milage may vary.

## Errors

If the file can't be processed, or if it does not contain text, you'll see `*** ERROR FOR FILE *** ` appear in the output, along with the link to the online file.  The script then proceeds to the next file.

* You can ignore .png files with this error, it means there was no text.
* You should manually inspect the .svg and .gif files.

## Future directions

* When I need it, I'll modify this to search for multiple terms, right now I'm just looking for one.

 * I didn't know of a good way to get a list of files from the online repo, which is why I used my local clone to find the file names of the images I'm interested in.  Perhaps there is a better way to do it all online, but for now this works for me!

* You could adapt the script to process local files, following the example from [OCR: Read File using the Read API, extract text - local](https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/ComputerVisionQuickstart.py#L99). Note the sleep time in that loop is 10 times larger than for online files. 

