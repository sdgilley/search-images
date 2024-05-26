# runs just the search_for_images function, 
# which searches for images in a repo and creates a csv file with the results
# does not look for .md files that use the images

import search_for_images as s
# *** PUT YOUR DETAILS HERE  *****
# what to search for - can be one or more terms
find_text = ["Open project in VS Code"]             # Text to find in the images.  
case_sensitive = True                               # True or False
csv_fn = "open-project.csv"                         # Put results in this file
# where to search
repo_name = "MicrosoftDocs/azure-docs"  # repo to search
branch = "main"
media_path = 'articles/ai-studio/media'  # point to the media dir you want to search
>>>>>>> 979227c004af0c9c861c74324aeb9e21c5c1db78
# or here's fabric:
# repo_name = "MicrosoftDocs/fabric-docs"
# branch = "main"
# media_path = 'docs/data-science/media' 

# *** END OF SEARCH DETAILS ***

# search for the images and create csv and md files with the results
s.search_for_images(find_text, case_sensitive,csv_fn, repo_name, branch, media_path)