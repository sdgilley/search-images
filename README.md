# search-images: Find text inside images

![search-images](media/search-for-text.png)

How to solve a (not so theoretical) problem:

> I'm documenting a UI, and a term in the UI has changed.  How do I find all the images that use this term?  I have 100s (or even 1000s) of images, and I don't want to have to open each one!

The **search-images.py** Python script searches for text inside images! It's set up to search for images in any **media** folder inside [MicrosoftDocs/azure-docs](https://github.com/MicrosoftDocs/azure-docs).  It creates a .csv file listing the files that match your search phrase.  

## Prerequisite

* Run [Quickstart: Optical character recognition (OCR)](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/client-library?tabs=visual-studio&pivots=programming-language-python
).  

* Install the PyGithub package

    ```console
    pip install PyGithub  
    ```

* Create a [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). In step 11, select **Public Repositories (read-only)** to search through that public repo, azure-docs.  If you want to search the private repo or your fork, specify the access details to that repository. 

* Create the following environment variables to be accessed when you run the Python script:
    * `GH_ACCESS_TOKEN` - the token you created from Github
    * `COMPUTER_VISION_ENDPOINT` - the endpoint you created from the OCR Quickstart
    * `COMPUTER_VISION_SUBSCRIPTION_KEY` - the key you created from the OCR Quickstart


> 📘 BEFORE YOU START - Clean up your images folder!
> 
> Save yourself time by first deleting images that are no longer in use.  For Microsoft articles, use the [Repo cleanup tool](https://review.learn.microsoft.com/help/contribute/clean-repo-tool?branch=main) to get rid of orphaned images.

## Run the script

1. Edit the file **search-image.py** and fill out the `PUT YOUR DETAILS HERE` section with your values.  This is where you say what to search for, where to search, and where to write results.

1. Run **search-images.py**.
    * Go grab a coffee, go to lunch, or find something else to work on.  
    * For 600 images, the script took approximately 15 minutes to complete. Your milage may vary.

## Results

Results are printed to the screen, so that you can watch the progress.  They are also added to a .csv file.

* If the file contains the search term, it is added to the results with a status of "found".
* If the file can't be processed, it is added to the results with a status of "unknown".  You'll need to manually inspect these files.
* If the file doesn't contain the search term, you won't see it it in the results.


## Future directions

* When I need it, I'll modify this to search for multiple terms, right now I'm just looking for one.
* Search is case sensitive.  Modify if necessary to make it case insensitive/
* You could adapt the script to process local files, following the example from [OCR: Read File using the Read API, extract text - local](https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/ComputerVisionQuickstart.py#L99). Note the sleep time in that loop is 10 times larger than for online files. 
