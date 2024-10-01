import requests
import os

# Fetch environment variables for authentication and repository details
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub Personal Access Token
REPO_OWNER = os.getenv("REPO_OWNER")  # Repository owner (user or org)
REPO_NAME = os.getenv("REPO_NAME")  # Repository name
BRANCH = os.getenv("DEPLOY_BRANCH")  # The branch to protect (e.g., main)

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set.")

# GitHub API URL to set branch protection
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{BRANCH}/protection"

# Headers for authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.luke-cage-preview+json"
}

# Branch protection settings payload
payload = {
    "required_status_checks": None,  # No status checks for now
    "enforce_admins": True,  # Enforce rules for admins
    "required_pull_request_reviews": {
        "dismissal_restrictions": {},
        "require_code_owner_reviews": True,  # Require reviews from CODEOWNERS
        "required_approving_review_count": 2  # Require two approving reviews
    },
    "restrictions": None,  # No restrictions on who can push
    "required_linear_history": True,
    "allow_force_pushes": False,
    "allow_deletions": False
}

# Send the PUT request to GitHub API to set the branch protection rules
response = requests.put(url, json=payload, headers=headers)

if response.status_code == 200:
    print(f"Branch protection successfully applied to {BRANCH}")
else:
    print(f"Failed to apply branch protection: {response.status_code} {response.text}")
