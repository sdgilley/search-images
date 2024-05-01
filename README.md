# search-images: Find text inside images

![search-images](media/search-for-text.png)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sdgilley/search-images?quickstart=1)

(Make sure to complete the [prerequisites](#prerequisites) before trying to run the code!)

### How to solve a (not so theoretical) problem:

> I'm documenting a UI, and a term in the UI has changed.  How do I find all the images that use this term?  I have 100s (or even 1000s) of images, and I don't want to have to open each one!

The **search-images.py** Python script searches for your text inside images. It's set up to search for images in any **media** folder inside a public repository, such as [MicrosoftDocs/azure-docs](https://github.com/MicrosoftDocs/azure-docs).  

The script creates a .csv file listing the files that match your search phrase, and a .md file with a preview of each image.

Modify the top part of the script to search for your own text, in your own repo.  You can also modify the script to search for multiple terms, and specify whether or not the match is case sensitive.


## Prerequisites

* Create a [Computer Vision resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision) in the Azure portal to get your key and endpoint. After it deploys, click **Go to resource**.

    * You will need the key and endpoint from the resource you create to connect your application to the Computer Vision service. Add your key and endpoint as environment variables as shown below.
    * You can use the free pricing tier (`F0`) to try the service, and upgrade later to a paid tier for production.

* Create a [GitHub personal access token (classic)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

    * To search from a public repo (such as azure-docs), you can leave all options unchecked.  Modify as necessary if you want to read a private repo instead.
    * Make sure to copy the token as soon as it's created.  Once you move away, you'll never see it again.
    * AFTER you've copied the token, use the **Configure SSO** dropdown to authorize **MicrosoftDocs**.

### Run on Codespaces

Python installs are all done for you if you use a codespace.  But first save the above values as secrets:
* Go to [Codespace secrets](https://github.com/settings/codespaces).
* Save each of the following:  
    * `GH_ACCESS_TOKEN` - the token you created from Github
    * `COMPUTER_VISION_ENDPOINT` - the endpoint you created from the OCR Quickstart
    * `COMPUTER_VISION_SUBSCRIPTION_KEY` - the key you created from the OCR Quickstart
 * Allow access to **sdgilley/search-images** for each secret.
 * Once your secrets are saved, use the Codespace button to create a codespace.  Later, the same button will reconnect to the same codespace.
    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sdgilley/search-images?quickstart=1)

### Run locally

If you want to run this in VS Code locally instead of a Codespace, see [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial).  Save the above secrets as environment variables, and install the following packages:

    ```console
    pip install --upgrade azure-cognitiveservices-vision-computervision
    pip install pillow
    pip install PyGithub  
    ```

> ## ⚠️ BEFORE YOU START - Clean up your images folder!
>
> Save yourself time by first deleting images that are no longer in use.  For Microsoft articles, use the [Repo cleanup tool](https://review.learn.microsoft.com/help/contribute/clean-repo-tool?branch=main) to get rid of orphaned images.

## Run the script

1. Edit the file **search-image.py** and fill out the `PUT YOUR DETAILS HERE` section with your values.  This is where you say what to search for, where to search, and where to write results.

1. Run **search-images.py**.
    * Go grab a coffee, go to lunch, or find something else to work on.  
    * For 600 images, the script took approximately 15 minutes to complete. Your milage may vary.

## Results

Results are printed to the screen, so that you can watch the progress.  They are also added to a .csv file and a .md file (the .md file shows a preview of each image).

* If the file contains the search term, it is added to the results with status showing the term found.
* If the file can't be processed, it is added to the results with a status of "unknown".  You'll need to manually inspect these files.
* If an image doesn't contain the search term, you won't see it it in the results.


