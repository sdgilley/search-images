# search-images: Find text inside images

![search-images](media/search-for-text.png)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sdgilley/search-images?quickstart=1)

(Make sure to complete the [prerequisites](#prerequisites) before trying to run the code!)

### How to solve a (not so theoretical) problem:

> I'm documenting a UI, and a term in the UI has changed.  How do I find all the images that use this term?  I have 100s (or even 1000s) of images, and I don't want to have to open each one!

The **search-images.py** Python script searchs for your text inside images. It's set up to search for images in any **media** folder inside a public repository, such as [MicrosoftDocs/azure-docs](https://github.com/MicrosoftDocs/azure-docs).  

The output from this script is a .csv file listing the files that match your search phrase, and a .md file with a preview of each image. 

Modify the top part of the script to search for your own text (one or more terms), in your own repo.  You can also specify whethr or no9t the match is case sensitive.

Scroll down to the last line - comment it out to save some time, or uncomment it to add additional a search of the files in the repo that use the images.  This will add an additional column to the .csv file, and a link to the .md file that uses the image.  You'll also get a -not-found.csv file with a list of the images that weren't found in any .md files.

## Authentication

I've gotten this to work with both Entra ID and Key authentication.  But when creating the resource on my BAMI account, I wasn't able to get access with Entra ID, while I was with key.  The default for now is Key.  You can switch it in the **search-images.py** file.  Instructions below include setup for both methods.

## Prerequisites

* Create an [Azure AI Services resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne) in the Azure portal. After it deploys, select **Go to resource**.

    * To use Entra ID: Select Access control (IAM).  Add a new role, **Cognitive Services User** (Make sure it is *User*, not *Contributor*). Assign yourself to this role. (This step necessary only if using Entra ID authentication.  Ignore for key authentication.)
    * Select Overview to find the endpoint. You'll need it below, for either type of authentication.

* Create a [GitHub personal access token (classic)][(https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic](https://github.com/settings/tokens)).

    * You can leave all options unchecked.
    * Make sure to copy the token as soon as it's created.  Once you move away, you'll never see it again.
    * AFTER you've copied the token, use the **Configure SSO** dropdown to authorize **MicrosoftDocs**.

* Login to CLI (Needed only when using Entra ID authentication)

    * Use `az login` to log into your account.  
    * If you are in a Codespace, use `az login --use-device-code`.
    * If you have access to lots of subscriptions, make sure the default is the subscription where you created the service.  
    * Use `az account set --subscription <SubscriptionName>` to set the default if necessary.

### Run on Codespaces

Python installs are all done for you if you use a codespace.  But first save the above values as secrets:

* Go to [Codespace secrets](https://github.com/settings/codespaces).
* Save each of the following:  
    * `GH_ACCESS_TOKEN` - the token you created from Github
    * `COMPUTER_VISION_ENDPOINT` - the endpoint from the service Overview page.
    * If using key authentication: `COMPUTER_VISION_SUBSCRIPTION_KEY` - the key from the service Keys page.
 * Allow access to **sdgilley/search-images** for each secret.
 * Once your secrets are saved, use the Codespace button to create a codespace.  Later, the same button will reconnect to the same codespace.

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sdgilley/search-images?quickstart=1)

### Run locally

If you want to run this in VS Code locally instead of a Codespace, see [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial).  Save the above secrets as environment variables, and install the following packages:

    ```console
    pip install --upgrade azure-cognitiveservices-vision-computervision
    pip install pillow
    pip install PyGithub
    pip install azure-identity
    ```

> ## ⚠️ BEFORE YOU START - Clean up your images folder!
>
> Save yourself time by first deleting images that are no longer in use.  For Microsoft articles, use the [Repo cleanup tool](https://review.learn.microsoft.com/help/contribute/clean-repo-tool?branch=main) to get rid of orphaned images.

## Run the script

1. Edit the file **search-images.py** and fill out the `PUT YOUR DETAILS HERE` section with your values.  This is where you say what to search for, where to search, and where to write results.
1. If you want to also see which .md file uses each image, uncomment the last line (`find-refs`). Or comment it out if you don't want this extra step.  
1. Run **search-images.py**.
    * Go grab a coffee, go to lunch, or find something else to work on.  
    * For 600 images, the script took approximately 15 minutes to complete. Your milage may vary.
    * The script will first find the images, then search for the .md file that uses each image.  It will creates two files in an **outputs** folder:
        * A .csv file listing the files that match your search phrase. It has two columns, the image file and the search term.
        * A .md file with a preview of each image.
    * If you also ran the last line (`find-refs`), The .csv has an additional column, the .md file that uses the image.  The .md file will also contain a link to the .md file that uses the image.
    * When you run `find-refs`, you'll also get a additional -not-found.csv file with a list of the images that weren't found in any .md files.  You can use this to clean up your images folder.

## Results

Results are printed to the screen, so that you can watch the progress.  They are also added to .csv and .md files in the **outputs** folder.

* If the file contains the search term, it is added to the results with status indicating which term was found.
* If the file can't be processed, it is added to the results with a status of "unknown".  You'll need to manually inspect these files.
* If an image doesn't contain the search term, you won't see it it in the results.
* Use the resulting .md file to preview all the images that contain the search term.