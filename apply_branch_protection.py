import requests
import os

# Get environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPOSITORY = os.getenv("GITHUB_REPOSITORY")
BRANCH = os.getenv("BRANCH", "main")
REVIEWERS = os.getenv("REVIEWERS").split(',')

# Define the API URL for branch protection
url = f"https://api.github.com/repos/{REPOSITORY}/branches/{BRANCH}/protection"

# Define branch protection rules payload
payload = {
        "required_status_checks": None,
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": False,
            "require_code_owner_reviews": True,
            "required_approving_review_count": 2
        },
        "restrictions": None,  # Could specify branch restrictions here
        "allow_force_pushes": False,
        "allow_deletions": False
    }
    
# Check if GITHUB_TOKEN exists
if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN is missing!")
    exit(1)  # Exit the script with a non-zero status code to indicate failure

# Set headers with the token for authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.luke-cage-preview+json"
}

# Send the request to update branch protection
response = requests.put(url, headers=headers, json=payload)

if response.status_code == 200:
    print(f"Branch protection rules updated for {branch} branch")
elif response.status_code == 403:
    print(f"Failed to apply branch protection rules: {response.status_code} - {response.json()}")
    print("Check your token permissions and ensure you have admin access.")
else:
    print(f"Error: {response.status_code} - {response.text}")

# Add code owners as reviewers to the PR
pr_number = os.getenv("GITHUB_PR_NUMBER")
if pr_number:
    reviewers_url = f"https://api.github.com/repos/{REPOSITORY}/pulls/{pr_number}/requested_reviewers"
    reviewer_payload = {
        "reviewers": REVIEWERS
    }

    review_response = requests.post(reviewers_url, headers=headers, json=reviewer_payload)

    if review_response.status_code == 201:
        print(f"Reviewers {REVIEWERS} successfully added to PR #{pr_number}.")
    else:
        print(f"Failed to add reviewers: {review_response.status_code}")
        print(review_response.json())
