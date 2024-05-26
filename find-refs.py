# find documents that display the images found in the .csv fileimport os
# runs just the search_md_files function, assumes you already have a .csv file with images of interest

import time
import datetime
import csv
import os
import search_md_files as s

script_dir = os.path.dirname(os.path.realpath(__file__))

###################### INPUT HERE ############################
# Name the path to your repo. If trying to use a private repo, you'll need a token that has access to it.
repo_name = "MicrosoftDocs/azure-docs"
repo_branch = "main"
path_in_repo = 'articles/ai-studio' 
# specify what to read from and what to write
image_fn = os.path.join(script_dir,"open-project.csv") # csv file with terms and images
result_fn = os.path.join(script_dir,"open-project-final.csv") # write results including md file
############################ DONE ############################
result_md = result_fn.split(".")[0] + ".md"  # Put previews in markdown file

# Step 1: Read the .csv file and store the terms and their corresponding images in a dictionary
terms_images = {}
with open(image_fn, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip the first line
    for row in reader:
        term, image = row  # assuming term is in the first column and image is in the second column
        terms_images[image] = term

# Step 2: Search for the images in the .md files in the repo
# Start search 
st = time.time()
print(f"===== Start .md searching for images from {image_fn} in {repo_name}/{repo_branch}/{path_in_repo} ====")
print(str(datetime.datetime.now()))
result = s.search_md_files(terms_images, repo_name, repo_branch, path_in_repo)

# Step 3: Write the result to a .csv file
with open(result_fn, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["term","image_file","md_file"])
    for row in result:
        writer.writerow(row)
with open(result_md, 'w', newline='') as m:
    for row in result:
        term, image, file = row
        m.write(f"{term}: {image} in {file}\n")
        m.write(f"<img src='{image}' width=500 >\n\n")

# list image that were not found in a .md file
not_found = set(terms_images.keys()) - set([row[1] for row in result])
# print(not_found)
with open("not_found.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["These images were not found in an .md file:"])
    for row in not_found:
        writer.writerow(row)
print (f"Done - see results in {result_fn}, {result_md}, and not_found.csv")
et = time.time()
elapsed = (et - st)/60
print(f" Execution time: {elapsed} minutes")
