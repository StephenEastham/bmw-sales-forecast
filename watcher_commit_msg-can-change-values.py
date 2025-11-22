# watcher_commit_msg.py
import os
import subprocess
import json
import sys
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory

# --- Configuration ---
# IMPORTANT: Set this to the repository you are working with in GitHub Desktop
REPO_ROOT = r'C:\Users\easts\github\bmw-sales-forecast'
# How many recent commit messages to load (will fetch more and filter by author)
COMMIT_LIMIT = 1000
# List of author names to filter by (show only commits from these authors)
AUTHOR_NAMES = ['StephenEastham', 'easts']
# Time period in days to look back for commits
TIME_PERIOD_DAYS = 30

# --- Helper Functions ---
def run_git(args):
    """Runs a git command and returns stdout."""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=False,
        )
        if result.returncode != 0:
            print(f"Git command error: {result.stderr.strip()}", file=sys.stderr)
            return ""
        return result.stdout.strip()
    except FileNotFoundError:
        print("Error: 'git' command not found. Is Git installed and in your PATH?", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Error running git command: {e}", file=sys.stderr)
        return ""

def get_commit_messages(days=TIME_PERIOD_DAYS):
    """Gets recent commit messages from the repository, filtered by author and deduplicated."""
    # Get current branch name
    current_branch = run_git(['symbolic-ref', '--short', 'HEAD'])
    if not current_branch:
        current_branch = "unknown"
    
    # Use git log with a format that includes the author name
    # %H = full hash, %ai = author date ISO format, %an = author name, %s = subject
    log_format = "%H|||%ai|||%an|||%s"
    
    # Calculate date based on the 'days' parameter
    start_date = datetime.now() - timedelta(days=days)
    since_date = start_date.strftime('%Y-%m-%d')
    
    output = run_git(['log', f'--since={since_date}', f'--pretty=format:{log_format}%n'])
    
    if not output:
        print("Warning: No commits found in repository.", file=sys.stderr)
        return [], since_date, current_branch

    # Dictionary to track unique messages (message -> commit info)
    # We keep only the most recent commit for each unique message
    unique_messages = {}
    lines = output.strip().split('\n')
    
    for line in lines:
        if not line.strip():
            continue
        parts = line.split('|||')
        if len(parts) >= 4:
            author = parts[2].strip()
            # Filter by author names in AUTHOR_NAMES
            if author in AUTHOR_NAMES:
                message = parts[3].strip()
                commit_info = {
                    "hash": parts[0][:7],  # Short hash
                    "date": parts[1],
                    "author": author,
                    "message": message
                }
                
                # Only add if we haven't seen this message before
                # (since we're iterating in reverse chronological order, the first occurrence is the most recent)
                if message not in unique_messages:
                    unique_messages[message] = commit_info
                
                if len(unique_messages) >= COMMIT_LIMIT:
                    break
    
    # Convert to list, maintaining order
    messages = list(unique_messages.values())
    date_range = f"{since_date} - {datetime.now().strftime('%m/%d/%Y')}"
    print(f"Loaded {len(messages)} unique commits from {AUTHOR_NAMES} in last {days} days on branch '{current_branch}' ({date_range}).", file=sys.stderr)
    return messages, since_date, current_branch

# --- Flask Web Server ---
app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main HTML file."""
    return send_from_directory('.', 'commit_messages-can-change-values.html')

@app.route('/commits')
def list_commits():
    """Return a list of recent commit messages."""
    try:
        days = request.args.get('days', default=TIME_PERIOD_DAYS, type=int)
        commits, since_date, current_branch = get_commit_messages(days=days)
        print(f"Returning {len(commits)} commits to client from branch '{current_branch}'.", file=sys.stderr)
        return jsonify({
            'commits': commits,
            'time_period_days': days,
            'since_date': since_date,
            'current_branch': current_branch
        })
    except Exception as e:
        print(f"Error in /commits endpoint: {e}", file=sys.stderr)
        return jsonify({'error': str(e), 'commits': [], 'time_period_days': 0, 'current_branch': 'unknown'}), 500

if __name__ == '__main__':
    if not os.path.isdir(REPO_ROOT) or not os.path.isdir(os.path.join(REPO_ROOT, '.git')):
        print(f"Error: Repository path '{REPO_ROOT}' is not a valid Git repository.", file=sys.stderr)
        print("Please update the REPO_ROOT variable in this script.", file=sys.stderr)
        sys.exit(1)

    print("Starting Flask server for commit messages...")
    print(f"Watching repository: {REPO_ROOT}")
    print("Open http://127.0.0.1:5001/ in your browser.")
    print("Press Ctrl+C to stop.\n")
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=True)
