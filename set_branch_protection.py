import os
import requests

# Load environment variables
GITHUB_TOKEN = os.getenv("TOKEN_GITHUB")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
BRANCH = os.getenv("BRANCH", "main")  # Default branch is 'main'

# GitHub API URL to update branch protection
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{BRANCH}/protection"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.luke-cage-preview+json"
}

# Payload to disallow direct pushes and require PRs
payload = {
    "required_status_checks": None,  # No status checks required for now
    "enforce_admins": True,  # Enforce protection for admins
    "required_pull_request_reviews": {
        "dismiss_stale_reviews": True,  # Dismiss stale reviews automatically
        "require_code_owner_reviews": False,  # Not requiring code owner reviews
        "required_approving_review_count": 1  # Require at least 1 approval
    },
    "restrictions": None,  # No restrictions on who can push once PR is approved
    "allow_force_pushes": False,  # Disallow force pushes
    "allow_deletions": False  # Disallow deletion of the branch
}

# Make the API call to GitHub to apply branch protection
response = requests.put(url, headers=headers, json=payload)

# Check response status
if response.status_code == 200:
    print(f"Branch protection applied successfully to '{BRANCH}'!")
else:
    print(f"Failed to apply branch protection: {response.status_code} - {response.text}")
