import requests
import yaml
import os

# Accessing environment variables from GitHub Actions
OWNER = os.getenv('REPO_OWNER')
REPO = os.getenv('REPO_NAME')
BRANCH = os.getenv('DEPLOY_BRANCH')
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

# Update branch protection rules
def update_branch_protection(settings):
    branch = settings['branch_protection']['branch']
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/branches/{branch}/protection"

    # Payload for branch protection rules
    payload = {
        "required_status_checks": None,  # No status checks enforced
        "enforce_admins": settings['branch_protection'].get('enforce_admins', True),
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": False,
            "require_code_owner_reviews": True,
            "required_approving_review_count": settings['branch_protection']['require_pull_request_reviews']['required_approving_review_count']
        },
        "restrictions": {
            "users": settings['branch_protection']['require_pull_request_reviews']['reviewers'],
            "teams": []
        },
        "allow_force_pushes": settings['branch_protection'].get('allow_force_pushes', False),
        "allow_deletions": settings['branch_protection'].get('allow_deletions', False)
    }

    # Make PUT request to update the branch protection rules
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Branch protection for '{branch}' updated successfully!")
    else:
        print(f"Failed to update branch protection: {response.status_code}, {response.text}")

# Ensure deployments only from the main branch
def setup_prod_deployments(settings):
    deploy_branch = settings['deployments']['prod_deploy_branch']
    if deploy_branch == "main":
        print(f"Production deployments restricted to the '{deploy_branch}' branch.")
    else:
        print("Please ensure production deployments happen from the 'main' branch.")

if __name__ == "__main__":
    # Load settings from the YAML file
    repo_settings = load_settings_from_yaml("repo_settings.yaml")
    
    # Update branch protection rules
    update_branch_protection(repo_settings)
    
    # Setup production deployments from main branch
    setup_prod_deployments(repo_settings)
