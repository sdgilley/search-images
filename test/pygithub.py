# This script accesses environment variable:
#     GH_ACCESS_TOKEN
# This script needs the following package:
#     pip install PyGithub

# testing out the Github API - trying it out here before I use it in search-images.py
from github import Github

# use this to form url to the raw images
online_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/"

# First create a Github instance:
# using an access token
import os

token = os.environ["GH_ACCESS_TOKEN"]
g = Github(token)

repo = g.get_repo("MicrosoftDocs/azure-docs")
contents = repo.get_contents("articles/ai-studio/media")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        img_url = online_url + file_content.path
        print(img_url)
