import os
import requests
import json

def update_branch_protection(owner, repo, branch, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "required_status_checks": {
            "strict": True,
            "contexts": []  # Specify required status checks here if needed
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": True,
            "required_approving_review_count": 1  # Minimum number of approvers
        },
        "restrictions": None,
        "allow_force_pushes": False,
        "allow_deletions": False
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Successfully updated branch protection for {branch}.")
    else:
        print(f"Failed to update branch protection: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    # Set your repository details
    owner = os.getenv("GITHUB_REPOSITORY").split("/")[0]  # Extract owner from the repository name
    repo = os.getenv("GITHUB_REPOSITORY").split("/")[1]  # Extract repo from the repository name
    branch = "main"  # The branch to protect
    token = os.getenv("TOKEN_GITHUB")  # Access token

    # Call the function to update branch protection
    update_branch_protection(owner, repo, branch, token)
