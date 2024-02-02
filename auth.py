# *** AUTHENTICATE 
import os
import sys
from github import Github

def get_auth_response(repo_name):

    # Get GH access token from environment variables (assumes you've exported this)
    # try to read GH_ACCESS_TOKEN from environment variables
    # if not there, tell user to set it
    try:
        token = os.environ['GH_ACCESS_TOKEN']   
    except:
        print("Please set GH_ACCESS_TOKEN environment variable")
        sys.exit()  

    g = Github(token)
    repo = g.get_repo(repo_name)

    # Authenticate with key, endpoint from environment variables (assumes you've exported these)
    # if not there, tell user to set it
    try:    
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
    except:
        print("Please set COMPUTER_VISION_ENDPOINT environment variable")
        sys.exit()

    try:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    except:
        print("Please set COMPUTER_VISION_SUBSCRIPTION_KEY environment variable")
        sys.exit()
    # *** End of Authenticate - you're now ready to run the script.
    return(endpoint, subscription_key, repo)