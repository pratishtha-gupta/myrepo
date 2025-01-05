import requests
import os
from datetime import datetime

# Define your Codeforces handle and repository path
CODEFORCES_HANDLE = "pratishthagupta"  # Replace with your handle
GITHUB_REPO_PATH = os.getcwd()  # Assumes the script is in the repo folder

def fetch_submissions(handle):
    """
    Fetches submissions from Codeforces API for the given handle.
    """
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f"Error fetching submissions: {response.status_code}")
        return []

def save_submission_to_git(submission):
    print(submission)  # Print the submission to check if it's being processed
    problem_name = submission['problem']['name']
    lang = submission['programmingLanguage']
    submission_time = datetime.utcfromtimestamp(submission['creationTimeSeconds']).strftime('%Y-%m-%d %H:%M:%S')
    file_name = f"{problem_name.replace(' ', '_')}.txt"
    file_path = os.path.join(os.getcwd(), file_name)

    if submission['verdict'] == 'OK':  # Only process successful submissions
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(f"Problem: {problem_name}\n")
                f.write(f"Language: {lang}\n")
                f.write(f"Submitted on: {submission_time}\n")
            commit_to_git(file_name)  # Commit the file after saving
        else:
            print(f"Skipped (already exists): {file_name}")
    else:
        print(f"Skipped (unsuccessful): {problem_name}")
def commit_to_git(file_name):
    print(f"Running Git commands for: {file_name}")  # Add this for debugging
    os.system(f"git add {file_name}")
    os.system(f'git commit -m "Added submission for {file_name}"')
    os.system("git push origin main")  # Make sure you're pushing to the correct branch
    print(f"Committed: {file_name}")


def main():
    """
    Main function to fetch submissions and save them to the repository.
    """
    # Fetch submissions from Codeforces
    submissions = fetch_submissions(CODEFORCES_HANDLE)
    for submission in submissions:
        if submission['verdict'] == 'OK':  # Only process successful submissions
            save_submission_to_git(submission)

if __name__ == "__main__":
    main()
