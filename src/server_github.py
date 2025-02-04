from mcp.server.fastmcp import FastMCP
from github import Github
import os
import json

mcp = FastMCP("github", dependencies=["PyGithub"])

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)

@mcp.tool()
def create_issue(title: str, body: str = "", labels: str = "", assignees: str = "", repo_name: str = os.getenv("REPO_NAME", "kyryl-opens-ml/mcp-webinar")) -> str:
    """
    Create a new GitHub issue in the specified repository.

    Parameters:
      - title (str): The title of the issue.
      - body (str): The content/description of the issue.
      - labels (str): Comma-separated list of labels to add to the issue.
      - assignees (str): Comma-separated list of GitHub usernames to assign the issue to.
      - repo_name (str): The repository name where the issue should be created.

    Returns:
      A string confirming the issue creation with a URL to the issue.
    """
    repo = g.get_repo(repo_name)
    # Convert comma-separated strings into lists (if provided)
    label_list = [label.strip() for label in labels.split(",")] if labels else []
    assignee_list = [assignee.strip() for assignee in assignees.split(",")] if assignees else []
    
    issue = repo.create_issue(
        title=title,
        body=body,
        labels=label_list,
        assignees=assignee_list
    )
    return f"Issue created: {issue.html_url}"

@mcp.tool()
def list_issues(repo_name: str = os.getenv("REPO_NAME", "kyryl-opens-ml/mcp-webinar")) -> str:
    """
    Retrieve and return all issues from the specified GitHub repository.

    Parameters:
      - repo_name (str): The repository name from which to list issues.

    Returns:
      A JSON-formatted string containing a list of issues with details such as number, title, state, assignees, and URL.
    """
    repo = g.get_repo(repo_name)
    # Get all issues (both open and closed) from the repository
    issues = repo.get_issues(state="all")
    issues_list = []
    for issue in issues:
        issues_list.append({
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
            "assignees": [assignee.login for assignee in issue.assignees],
            "url": issue.html_url,
        })
    return json.dumps(issues_list, indent=2)

@mcp.tool()
def remove_all_issues(repo_name: str = os.getenv("REPO_NAME", "kyryl-opens-ml/mcp-webinar")) -> str:
    """
    Remove all issues from the specified GitHub repository.

    Parameters:
      - repo_name (str): The repository name in which to remove all issues.

    Returns:
      A string confirming the removal of all issues.
    """
    repo = g.get_repo(repo_name)
    # Get all issues (both open and closed) from the repository
    issues = repo.get_issues(state="all")
    for issue in issues:
        issue.edit(state="closed")
    return "All issues have been closed."

@mcp.tool()
def update_issue(issue_number: int, title: str = "", body: str = "", labels: str = "", assignees: str = "", repo_name: str = os.getenv("REPO_NAME", "kyryl-opens-ml/mcp-webinar")) -> str:
    """
    Update an existing GitHub issue with new details.

    Parameters:
      - issue_number (int): The number of the issue to update.
      - title (str): The new title for the issue (leave empty to retain current title).
      - body (str): The new content/description for the issue (leave empty to retain current body).
      - labels (str): Comma-separated list of new labels (leave empty to retain current labels).
      - assignees (str): Comma-separated list of new assignees (leave empty to retain current assignees).
      - repo_name (str): The repository name where the issue exists.

    Returns:
      A string confirming the update of the issue with the updated issue URL.
    """
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)
    update_fields = {}

    if title:
        update_fields["title"] = title
    if body:
        update_fields["body"] = body
    if labels:
        update_fields["labels"] = [label.strip() for label in labels.split(",")]
    if assignees:
        update_fields["assignees"] = [assignee.strip() for assignee in assignees.split(",")]

    if not update_fields:
        return "No updates provided."

    issue.edit(**update_fields)
    return f"Issue updated: {issue.html_url}"

if __name__ == "__main__":
    mcp.run(transport='stdio')