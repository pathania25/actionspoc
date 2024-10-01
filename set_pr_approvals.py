import os
import requests

# Load environment variables (replace with your own tokens, repo, and branch)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub Personal Access Token
REPO_OWNER = os.getenv("REPO_OWNER")  # Repository owner (user or org)
REPO_NAME = os.getenv("REPO_NAME")  # Repository name
BRANCH = os.getenv("DEPLOY_BRANCH")  # The branch to protect (e.g., main)

# GitHub API URL for updating branch protection
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{BRANCH}/protection"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.luke-cage-preview+json"
}

payload = {
    "required_pull_request_reviews": {
        "dismiss_stale_reviews": True,
        "require_code_owner_reviews": True,
        "required_approving_review_count": 2  # Require at least 2 approvals
    },
    "restrictions": {
        "users": [],  # No user restrictions, just CODEOWNERS
        "teams": []   # No team restrictions
    },
    "allow_force_pushes": False,
    "allow_deletions": False
}

response = requests.put(url, headers=headers, json=payload)

if response.status_code == 200:
    print(f"PR approvals set for '{BRANCH}' branch!")
else:
    print(f"Failed to set PR approvals: {response.status_code} - {response.text}")