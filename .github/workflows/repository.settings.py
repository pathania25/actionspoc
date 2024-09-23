import requests
import yaml

# Load configuration from YAML
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to update branch protection rule
def update_branch_protection(repo_owner, repo_name, branch, token, approvers):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch}/protection"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.luke-cage-preview+json"
    }

    payload = {
        "required_status_checks": {
            "strict": True,
            "contexts": []  # Add any required status checks here
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": True,
            "required_approving_review_count": 2
        },
        "restrictions": None,  # Could specify branch restrictions here
        "allow_force_pushes": False,
        "allow_deletions": False
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Branch protection rules updated for {branch} branch")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Function to enforce PR approvals
def set_code_owner_reviews(repo_owner, repo_name, branch, token, approvers):
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
def restrict_deployments(repo_owner, repo_name, branch, token):
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
    # Set up repository details
    repo_owner = os.getenv("REPO_OWNER")  # Replace with your GitHub username
    repo_name = os.getenv("REPO_NAME")   # Replace with your repository name
    branch = "main"
    token = os.getenv("TOKEN_GITHUB") # Replace with your GitHub PAT

    # Load the configuration from the YAML file
    config = load_config("repository_settings.yaml")

    # Apply branch protection rules
    branch_protection_rules = config['branch_protection_rules'][0]
    update_branch_protection(repo_owner, repo_name, branch, token, branch_protection_rules['required_approvers'])

    # Set PR approvals to require reviews from Ravi and Monika
    set_code_owner_reviews(repo_owner, repo_name, branch, token, branch_protection_rules['required_approvers'])

    # Restrict deployments to the main branch
    restrict_deployments(repo_owner, repo_name, branch, token)
