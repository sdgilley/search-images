"""
Function to search for md files that include images from the .csv file
input: terms_images - dictionary of terms and images
         repo_name - repository name
         repo_branch - branch name
         path_in_repo - path in the repository
output: result - list of tuples with term, image, and md file
"""


# search for md files that include images from the .csv file


def search_md_files(terms_images, repo_name, repo_branch, path_in_repo):
    import os
    import gh_auth as a

    # connect to docs
    repo = a.connect_repo(repo_name)
    contents = repo.get_contents(path_in_repo, ref=repo_branch)
    result = []
    for content_file in contents:
        if content_file.type == "dir":
            contents.extend(repo.get_contents(content_file.path))
        elif content_file.path.endswith(".md"):
            file = os.path.basename(content_file.path)
            # Get the file content
            file_content = content_file.decoded_content
            content = file_content.decode("utf-8")
            # Use a regular expression to find image references in the .md file content
            for image, term in terms_images.items():
                image_base = os.path.basename(image)
                if image_base in content:
                    file = f"https://github.com/{repo.full_name}/blob/{repo_branch}/{content_file.path}"
                    result.append((term, image, file))
    return result
