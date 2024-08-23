"""
Function to search through a csv file with images, and find the corresponding .md 
files that reference them
input: find_text - list of text to find in the images
            case_sensitive - True or False
            csv_fn - csv file to write results
            repo_name - repository name
            branch - branch name
            media_path - path to the media directory in the repository
output: csv and md files with the results, plus a not-found csv file

uses the helpers.search_md_files to perform the search
  
"""
import time
import datetime
import csv
import os
import helpers.search_md_files as s


# read the images results and find the .md files that use them.  Write unused images to a file
def find_refs(image_fn, repo_name, repo_branch, path_in_repo, result_basename):
    # NOTE: path_in_repo is the path to th folder where .md files are located, not the media folder!
    # add path to image_fn
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(script_dir)  # go up one directory from script_dir
    output_dir = os.path.join(parent_dir, "outputs")  # add "outputs" to the parent directory
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # form the output files: result_csv, result_md, and not_found_fn:
    result_csv = os.path.join(output_dir, f"{result_basename}.csv")  # write results in csv file
    result_md = os.path.join(output_dir, f"{result_basename}.md")  # write results in md file
    not_found_fn = os.path.join(output_dir, f"{result_basename}-not-found.csv")  # write not found images
    
    # Step 1: Read the .csv file with terms and images from image_fn
    terms_images = {}
    with open(image_fn, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip the first line
        for row in reader:
            (
                term,
                image,
            ) = row  # assuming term is in the first column and image is in the second column
            terms_images[image] = term

    # Step 2: Search for the images in the .md files in the repo
    # Start search
    st = time.time()
    print(
        f"===== Start .md searching for images from {image_fn} in {repo_name}/{repo_branch}/{path_in_repo} ===="
    )
    print(str(datetime.datetime.now()))
    result = s.search_md_files(terms_images, repo_name, repo_branch, path_in_repo)
    # form files:
    # Step 3: Write the result to a .csv file
    with open(result_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["term", "image_file", "md_file"])
        for row in result:
            writer.writerow(row)
    # write the md file as well
    with open(result_md, "w", newline="") as m:
        for row in result:
            term, image, file = row
            m.write(f"{term}: {image} in {file}\n")
            m.write(f"<img src='{image}' width=500 >\n\n")

    # list image that were not found in a .md file
    not_found = set(terms_images.keys()) - set([row[1] for row in result])
    # Convert the list to a string with each item on a new line
    not_found_str = "\n".join(not_found)
    not_found_str = "Images not found in the .md files:\n" + not_found_str
    # Write the string to the output file
    with open(not_found_fn, 'w') as output_file:
        output_file.write(not_found_str)

    print(f"Done - see results in {result_csv}, {result_md}, and {not_found_fn}")
    et = time.time()
    elapsed = (et - st) / 60
    print(f" Execution time: {elapsed} minutes")

# test the function
if __name__ == "__main__":
    ##################### INPUT HERE ############################
    csv_fn = "images.csv" 
    # Name the path to your repo. 
    repo_name = "MicrosoftDocs/azure-docs"
    repo_branch = "main"
    path_in_repo = "articles/ai-studio" # where the md files are
    ##################### END INPUT ################

    result_basename = os.path.basename(csv_fn).split(".")[0]
    # run the function
    find_refs(csv_fn, repo_name, repo_branch, path_in_repo, result_basename)
