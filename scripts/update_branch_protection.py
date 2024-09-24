import requests
import yaml
import os

# GitHub API token (ensure you have 'repo' permission)
GITHUB_TOKEN = os.getenv('TOKEN_GITHUB')

# Headers for GitHub API requests
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Load Repository settings from YAML file
def load_settings_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

# Function to apply branch protection
def apply_branch_protection(repo_owner, repo_name, protection_settings):
    branch = protection_settings['branch_protection']['branch']
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch}/protection"

    # Prepare payload for branch protection
    payload = {
        "required_status_checks": None,  # Disable status checks
        "enforce_admins": protection_settings['branch_protection'].get('enforce_admins', True),
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": protection_settings['branch_protection']['require_pull_request_reviews'].get('dismiss_stale_reviews', False),
            "required_approving_review_count": protection_settings['branch_protection']['require_pull_request_reviews'].get('required_approving_review_count', 1)
        },
        "restrictions": None if not protection_settings['branch_protection'].get('restrict_pushes', {}).get('enabled', False) else {
            "users": [],  # Optionally add specific users allowed to push
            "teams": []
        },
        "allow_force_pushes": protection_settings['branch_protection'].get('allow_force_pushes', False),
        "allow_deletions": protection_settings['branch_protection'].get('allow_deletions', False)
    }

    # Make PUT request to apply branch protection
    response = requests.put(url, headers=headers, json=payload)

    # Check if protection was successfully applied
    if response.status_code == 200:
        print(f"Branch protection for '{branch}' applied successfully!")
    else:
        print(f"Failed to apply branch protection: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Load configuration from YAML file
    config = load_yaml_config("branch_protection.yaml")

    # Define your GitHub repository owner and name
    OWNER = os.getenv('REPO_OWNER')
    REPO = os.getenv('REPO_NAME')
    BRANCH = os.getenv('DEPLOY_BRANCH')

    # Apply branch protection
    apply_branch_protection(REPO_OWNER, REPO_NAME, config)