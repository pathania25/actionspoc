import os
import requests

# Load GitHub Token from environment variables (set securely in GitHub Actions)
GITHUB_TOKEN = os.getenv("TOKEN_GITHUB")
OWNER = os.getenv("REPO_OWNER")  # Replace with your GitHub username or organization
REPO = os.getenv("REPO_NAME")   # Replace with your repository name
BRANCH = os.getenv("DEPLOY_BRANCH")  # Branch to apply protection to

# GitHub API URL for branch protection
url = f"https://api.github.com/repos/{OWNER}/{REPO}/branches/{BRANCH}/protection"

# Headers with authorization
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Payload for branch protection rules
payload = {
    "required_status_checks": None,  # No status checks required
    "enforce_admins": True,  # Enforce rules on admins
    "required_pull_request_reviews": {
        "dismiss_stale_reviews": True,
        "require_code_owner_reviews": True,  # Enforce CODEOWNERS review rules
        "required_approving_review_count": 1  # Require at least 1 approval
    },
   #"restrictions": {
   #     "users": ["Ravi", "Manasa"],  # Only allow Ravi and Manasa to push
   #     "teams": []  # You can add GitHub teams if needed
   #},
    "allow_force_pushes": False,  # Disable force pushes
    "allow_deletions": False      # Disable branch deletions
}

# Apply branch protection rules using the GitHub API
response = requests.put(url, headers=headers, json=payload)

# Check for successful response
if response.status_code == 200:
    print(f"Branch protection applied successfully to '{BRANCH}' branch!")
else:
    print(f"Failed to apply branch protection: {response.status_code} - {response.text}")
