import os
import requests

# Load environment variables
GITHUB_TOKEN = os.getenv("TOKEN_GITHUB")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
BRANCH = os.getenv("DEPLOY_BRANCH")

# GitHub API URL for updating branch protection
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{BRANCH}/protection"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.luke-cage-preview+json"
}

# Payload for branch protection
payload = {
    "required_status_checks": None,  # No required status checks for now
    "enforce_admins": True,  # Apply the protection to repository admins as well
    "required_pull_request_reviews": {
        "dismiss_stale_reviews": True,
        "require_code_owner_reviews": True,  # Require review from CODEOWNERS (Ravi, Manasa)
        "required_approving_review_count": 1  # Require at least one approval
    },
    "restrictions": None,  # No further restrictions on push
    "allow_force_pushes": False,
    "allow_deletions": False
}

# Make the API call to GitHub to set the branch protection rules
response = requests.put(url, headers=headers, json=payload)

if response.status_code == 200:
    print(f"Branch protection applied successfully to '{BRANCH}' branch!")
else:
    print(f"Failed to apply branch protection: {response.status_code} - {response.text}")
