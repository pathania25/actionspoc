import os
import requests

# Fetch environment variables for authentication and repository details
GITHUB_TOKEN = os.getenv("TOKEN_GITHUB")
REPO_OWNER = os.getenv("REPO_OWNER")  # Replace with your GitHub username or organization
REPO_NAME = os.getenv("REPO_NAME")   # Replace with your repository name
BRANCH = os.getenv("DEPLOY_BRANCH")  # Branch to apply protection to protect (e.g., 'main')

if not github_token:
    raise ValueError("GITHUB_TOKEN environment variable is not set.")

# GitHub API URL to set branch protection
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch_name}/protection"

# Headers for authentication
headers = {
    "Authorization": f"token {github_token}",
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
    print(f"Branch protection successfully applied to {branch_name}")
else:
    print(f"Failed to apply branch protection: {response.status_code} {response.text}")
