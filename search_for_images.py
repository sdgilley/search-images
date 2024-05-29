"""
Function to search for images in a reporitory
input: find_text - list of text to find in the images
            case_sensitive - True or False
            csv_fn - csv file to write results
            repo_name - repository name
            branch - branch name
            media_path - path to the media directory in the repository
output: csv and md files with the results

This function accesses environment variables 
     GH_ACCESS_TOKEN, COMPUTER_VISION_ENDPOINT, COMPUTER_VISION_SUBSCRIPTION_KEY
see readme for details

This script uses the following packages:
    pip install azure-ai-vision-imageanalysis
    pip install pillow
    pip install PyGithub  
"""


# function searches for the text and writes results to csv and md files
def search_for_images(find_text, case_sensitive, csv_fn, repo_name, branch, media_path):
    # form vars from search details above
    md_fn = csv_fn.split(".")[0] + ".md"  # Put previews in markdown file
    online_url = f"https://raw.githubusercontent.com/{repo_name}/{branch}/"  # to get raw images from the repo

    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    from azure.ai.vision.imageanalysis.models import VisualFeatures
    from azure.core.credentials import AzureKeyCredential
    import os
    import re

    import time
    import datetime
    from auth import get_auth_response

    # get vision tokens and the repo
    endpoint, key, repo = get_auth_response(repo_name)

    # Create an Image Analysis client
    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # open csv file to store results
    import csv

    # Write results to csv file
    f = open(csv_fn, "w+")
    # write header
    f.write("status,url\n")
    # add previews to an md file
    m = open(md_fn, "w+")
    m.write("# Previews of the found files\n\n")
    # initialize counts
    pr = 0
    counts = {text: 0 for text in find_text}
    unk = 0

    # Start search
    st = time.time()

    print(
        f"===== Start searching files for {find_text} in {repo_name}/{branch}/{media_path} ===="
    )
    print(str(datetime.datetime.now()))
    try:
        contents = repo.get_contents(media_path)
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                img_url = online_url + file_content.path
                try:
                    # analyze image
                    result = client.analyze_from_url(
                        image_url=img_url,
                        visual_features=[VisualFeatures.READ],
                    )
                    # if there are results
                    if result.read is not None:
                        pr += 1
                        # If find_text is found, add the image to the csv and md files
                        for text in find_text:
                            found = False
                            for line in result.read.blocks[0].lines:

                                # Case sensitive search
                                if case_sensitive:
                                    txt_found = (
                                        re.search(
                                            r"\b" + re.escape(text) + r"\b", line.text
                                        )
                                        is not None
                                    )
                                # Case insensitive search
                                else:
                                    txt_found = (
                                        re.search(
                                            r"\b" + re.escape(text) + r"\b",
                                            line.text,
                                            re.IGNORECASE,
                                        )
                                        is not None
                                    )
                                # txt_found = line.text.find(text) >= 0 if case_sensitive else line.text.lower().find(text.lower()) >= 0
                                if txt_found:
                                    found = True
                                    break
                            if found:
                                f.write(f"{text}, {img_url}\n")
                                m.write(f"{text}: {img_url}\n")
                                m.write(f"<img src='{img_url}' width=500 >\n\n")
                                print(f"FOUND {text}: {img_url}")
                                counts[text] += 1
                except:
                    if (
                        os.path.splitext(file_content.path)[1] != ".png"
                    ):  # dont care about png with no text
                        f.write("unknown, " + img_url)
                        f.write("\n")
                        unk += 1
                        print("Unknown: " + img_url)
                    else:
                        print(f"Error occurred reading image {img_url}")
    except Exception as e:
        print(f"An error occurred trying to read https://github.com/{repo_name}/tree/{branch}/{media_path}")
        print("Check the path and the repo name.")
        print(e)
        return
    
    f.close()
    m.close()

    et = time.time()
    elapsed = (et - st) / 60

    print(
        f"===== Done searching files for {find_text} in {repo_name}/{branch}/{media_path} ===="
    )
    print(f" Files processed:  {pr}")
    for text in find_text:
        print(f" Matches for {text}: {counts[text]}")
    print(f" Files to investigate: {unk}")
    print(f" See results in {csv_fn} and {md_fn}")
    print(f" Execution time: {elapsed} minutes")

    # results are  saved in the csv and md files
