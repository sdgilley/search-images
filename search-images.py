# runs both search_for_images and search_md_files functions
# creates multiple .csv files with results, also .md files and a not_found.csv file

import os
import helpers.search_for_images as s
import helpers.find_refs as f

# *** PUT YOUR DETAILS HERE  *****
# what to search for - can be one or more terms
find_text = ["Data Factory"]  # Text to find in the images.
case_sensitive = True  # True or False
ref_basename = "data-factory"  # base name for the results files
# where to search
# repo_name = "MicrosoftDocs/azure-docs"  # repo to search
# branch = "main"
# path_in_repo = "articles/ai-studio"  # where the md files are
# or here's fabric:
repo_name = "MicrosoftDocs/fabric-docs"
branch = "main"
path_in_repo = "docs/data-science"  # where the md files are

# *** END OF SEARCH DETAILS ***
media_path = f"{path_in_repo}/media"

import os
auth = "key" # set to any other value to use Entra ID
# search for the images and create initial csv and md files with the results
csv_fn = s.search_for_images(find_text, case_sensitive, ref_basename, repo_name, branch, media_path, auth)
# Uncomment the next line if you want to also find the .md file that references each image
f.find_refs(csv_fn, repo_name, branch, path_in_repo, ref_basename)