# runs both search_for_images and search_md_files functions
# creates multiple .csv files with results, also .md files and a not_found.csv file

import time
import datetime
import csv
import os
import search_for_images as s
import search_md_files as m

# *** PUT YOUR DETAILS HERE  *****
# what to search for - can be one or more terms
find_text = ["Open project in VS Code"]             # Text to find in the images.  
case_sensitive = True                               # True or False
csv_fn = "open-project.csv"                         # Put initial results in this file

# where to search
repo_name = "MicrosoftDocs/azure-docs"  # repo to search
branch = "main"
path_in_repo = 'articles/ai-studio' # where the md files are
media_path = f"{path_in_repo}/media"
# or here's fabric:
# repo_name = "MicrosoftDocs/fabric-docs"
# branch = "main"
# media_path = 'docs/data-science/media' 

# *** END OF SEARCH DETAILS ***

# create final filenames for results
filename, _ = os.path.splitext(os.path.basename(csv_fn))
result_fn = f"{filename}-final.csv"
result_md = f"{filename}-final.md"

# search for the images and create initial csv and md files with the results
s.search_for_images(find_text, case_sensitive, csv_fn, repo_name, branch, media_path)

# Read the .csv file and store the terms and their corresponding images in a dictionary
terms_images = {}
with open(csv_fn, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip the first line
    for row in reader:
        term, image = row  # assuming term is in the first column and image is in the second column
        terms_images[image] = term

# Search for the images in the .md files in the repo
# Start search 
st = time.time()
print(f"===== Start .md search for images from {csv_fn} in {repo_name}/{branch}/{path_in_repo} ====")
print(str(datetime.datetime.now()))
result = m.search_md_files(terms_images, repo_name, branch, path_in_repo)

# Write the result to the final .csv files
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
print(f" Execution time for .md search: {elapsed} minutes")
