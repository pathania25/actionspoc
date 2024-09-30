import os
import requests

# Load GitHub Token from environment variables (set securely in GitHub Actions)
GITHUB_TOKEN = os.getenv("TOKEN_GITHUB")
REPO_OWNER = os.getenv("REPO_OWNER")  # Replace with your GitHub username or organization
REPO_NAME = os.getenv("REPO_NAME")   # Replace with your repository name
BRANCH = os.getenv("DEPLOY_BRANCH")  # Branch to apply protection to

# GitHub API URL for updating branch protection
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{BRANCH}/protection"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

payload = {
    "required_status_checks": None,  # No required status checks for now
    "enforce_admins": True,  # Enforce protection for admins
    "required_pull_request_reviews": {
        "require_code_owner_reviews": True,
        "required_approving_review_count": 2  # Require at least 2 reviews
    },
    "restrictions": None,  # No additional restrictions
    "allow_force_pushes": False,
    "allow_deletions": False
}

response = requests.put(url, headers=headers, json=payload)

if response.status_code == 200:
    print(f"Branch protection applied to '{BRANCH}' branch!")
else:
    print(f"Failed to apply branch protection: {response.status_code} - {response.text}")