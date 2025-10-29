import csv
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from langchain_community.document_loaders.github import GitHubIssuesLoader
import os
from tqdm import tqdm

# GitHub token
ACCESS_TOKEN = "your token"

def parse_date(date_str):
    try:
        # Convert yy-mm-dd format to datetime object
        return datetime.strptime(date_str, '%y-%m-%d')
    except ValueError:
        return None

def extract_repo_info(github_link):
    # Extract username and repository name from GitHub link
    pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, github_link)
    if match:
        return match.group(1), match.group(2)
    return None, None

def get_issues_for_repo(owner, repo):
    try:
        loader = GitHubIssuesLoader(
            repo=f"{owner}/{repo}",
            access_token=ACCESS_TOKEN,
            include_prs=False,
            state="closed",
            since="2023-01-01T00:00:00Z",
        )
        return loader.load()
    except Exception as e:
        print(f"Error fetching issues ({owner}/{repo}): {str(e)}")
        return []

def process_github_links():
    try:
        # Create the issues_closed.csv file and write the header
        with open('issues_closed.csv', 'w', newline='', encoding='utf-8-sig') as issues_file:
            fieldnames = ['App Name', 'GitHub Link', 'F-Droid Link', 'Last Update Date', 'App Description', 'Category',
                         'Issue URL', 'Issue Title', 'Issue Creation Date', 'Issue Content']
            writer = csv.DictWriter(issues_file, fieldnames=fieldnames)
            writer.writeheader()

            # Read the original data
            with open('fdroid_data.csv', 'r', encoding='utf-8-sig') as file:
                csv_reader = csv.DictReader(file)
                # Convert csv_reader to a list to get total rows
                rows = list(csv_reader)
                
                # Use tqdm to create a progress bar
                for row in tqdm(rows, desc="Processing GitHub Repositories", unit="repo"):
                    # Check if the update date is after Jan 1, 2023
                    update_date = parse_date(row['Last Update Date'])
                    if not update_date or update_date < datetime(2023, 1, 1):
                        continue

                    github_link = row['GitHub Repository']
                    if not github_link:
                        continue

                    print(f"\nProcessing: {row['App Name']} - {github_link}")
                    owner, repo = extract_repo_info(github_link)
                    
                    if not owner or not repo:
                        print(f"Unable to parse GitHub link: {github_link}")
                        continue

                    issues = get_issues_for_repo(owner, repo)
                    
                    # Write a row for each issue
                    for issue in issues:
                        writer.writerow({
                            'App Name': row['App Name'],
                            'GitHub Link': github_link,
                            'F-Droid Link': row['F-Droid Link'],
                            'Last Update Date': row['Last Update Date'],
                            'App Description': row['App Description'],
                            'Category': row['Category'],
                            'Issue URL': issue.metadata.get('url', ''),
                            'Issue Title': issue.metadata.get('title', ''),
                            'Issue Creation Date': issue.metadata.get('created_at', ''),
                            'Issue Content': issue.page_content
                        })
                    
                    # input('stop here')

    except FileNotFoundError:
        print("Error: fdroid_data.csv file not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    process_github_links()
