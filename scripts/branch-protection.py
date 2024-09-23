import requests
import os

# Environment variables (Set these up in GitHub secrets or locally for testing)
GITHUB_TOKEN = os.getenv("TOKEN_GITHUB")  # GitHub PAT token
REPO_OWNER = os.getenv("REPO_OWNER")      # Owner of the repo (user or organization)
REPO_NAME = os.getenv("REPO_NAME")        # Repository name
BRANCH_NAME = "main"                      # Branch to protect

# GitHub API URL
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{BRANCH_NAME}/protection"

# Headers with authentication
headers = {
    "Authorization": f"token {TOKEN_GITHUB}",
    "Accept": "application/vnd.github.v3+json"
}

# Protection rules payload
payload = {
    "required_status_checks": {
        "strict": True,
        "contexts": []  # No specific status checks for now
    },
    "enforce_admins": True,  # Enforce for admins
    "required_pull_request_reviews": {
        "dismissal_restrictions": {
            "users": ["ravicharan-nettyam", "pathania25"],  # Replace with actual GitHub usernames
            "teams": []  # Can add specific teams if needed
        },
        "dismiss_stale_reviews": False,
        "require_code_owner_reviews": True,
        "required_approving_review_count": 2  # Require approvals from Ravi and Monika
    },
    "restrictions": {
        "users": [],
        "teams": []
    },
    "required_linear_history": True,  # Enforce linear history
    "allow_force_pushes": False,      # Disallow force pushes
    "allow_deletions": False          # Disallow branch deletions
}

# Send PUT request to GitHub API
response = requests.put(url, json=payload, headers=headers)

if response.status_code == 200:
    print(f"Branch protection applied successfully to {BRANCH_NAME}")
else:
    print(f"Failed to apply branch protection: {response.status_code} {response.text}")
