import requests
import yaml
import os

# Load configuration from YAML
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to update branch protection rule
def update_branch_protection(repo_owner, repo_name, branch, github_token, approvers):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch}/protection"

# Headers with authentication
headers = {
    "Authorization": f"token {token}",
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
        "dismiss_stale_reviews": True,
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
    print(f"Branch protection applied successfully to {branch}")
else:
    print(f"Failed to apply branch protection: {response.status_code} {response.text}")

# Function to enforce PR approvals
def set_code_owner_reviews(repo_owner, repo_name, branch, github_token, approvers):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch}/protection/required_pull_request_reviews"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.luke-cage-preview+json"
    }

    payload = {
        "require_code_owner_reviews": True,
        "required_approving_review_count": 2
    }

    response = requests.patch(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print(f"PR approvals set to require reviews from: {', '.join(approvers)}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Function to restrict deploys to main branch
def restrict_deployments(repo_owner, repo_name, branch, github_token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/environments/production"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.luke-cage-preview+json"
    }

    payload = {
        "deployment_branch_policy": {
            "protected_branches": True,
            "custom_branch_policies": False
        }
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Deployment restricted to {branch} branch")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Main function
if __name__ == "__main__":
    # Define your repository details
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")
    branch = "main"
    github_token = os.getenv("TOKEN_GITHUB")

    # Load the configuration from the YAML file
    config = load_config("protection-branch.yaml")

    # Apply branch protection rules
    branch_protection_rules = config['branch_protection_rules'][0]
    update_branch_protection(repo_owner, repo_name, branch, github_token, branch_protection_rules['required_approvers'])

    # Set PR approvals to require reviews from Ravi and Manasa
    set_code_owner_reviews(repo_owner, repo_name, branch, github_token, branch_protection_rules['required_approvers'])

    # Restrict deployments to the main branch
    restrict_deployments(repo_owner, repo_name, branch, github_token)
