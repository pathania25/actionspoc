import os
import requests

# Load environment variables
GITHUB_TOKEN = os.getenv("TOKEN_GITHUB")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
BRANCH_NAME = os.getenv("BRANCH_NAME", "main")  # Default to 'main'

def apply_branch_protection():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{BRANCH_NAME}/protection"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Define branch protection rules
    payload = {
        "required_status_checks": None,
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews": True
        },
        "restrictions": None  # No user restrictions
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Branch protection rules applied successfully.")
    else:
        print(f"Failed to apply branch protection: {response.status_code} - {response.text}")

if __name__ == "__main__":
    apply_branch_protection()
