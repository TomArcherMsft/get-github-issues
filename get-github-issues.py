from github import Github
import os
import urllib.request
import re
import argparse
from colorama import Fore, Back, Style

# Load GitHub application token from environment variable.
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Load Git login ID from environment variable.
GIT_LOGIN = os.environ.get("GIT_LOGIN")

# Load GitHub org name.
GITHUB_ORG = os.getenv('GITHUB_ORG')

# Constants
GITHUB_DOMAIN = 'https://github.com'

def print_error(msg):
  print(Fore.RED)
  print(msg)

def get_issues(repo_name):
	gh = Github(GITHUB_TOKEN)
	q_repo_name = f"{GITHUB_ORG}/{repo_name}"
	repo = gh.get_repo(q_repo_name)

	issues = repo.get_issues(state='open', assignee=GIT_LOGIN)
	return issues

def build_issue(repo_name, gh_issue):
	issue = {}
	issue['title'] = gh_issue.title
	issue['url'] = gh_issue.html_url
	issue['article_url'] = ""
	issue['product'] = ""

	response = urllib.request.urlopen(gh_issue.html_url)
	data = response.read()      # a `bytes` object as data is binary

	comments = data.decode('utf-8')

	content_source_pattern = re.compile('<li>Content Source: <a href="(.*?)"')
	content_source_match = content_source_pattern.search(comments)
	if content_source_match:
		issue['article_url'] = content_source_match.group(1)

	product_pattern = re.compile(f"{GITHUB_DOMAIN}/{GITHUB_ORG}/{repo_name}/blob/(main|master)/articles/(.*?)/")
	product_match = product_pattern.search(comments)
	if product_match:
		issue['product'] = product_match.group(2)

	return issue

def clean_up():
	print(Style.RESET_ALL)

def parse_args():
	argParser = argparse.ArgumentParser()
	argParser.add_argument("-r", "--repo", help="GitHub repository name.", required=True)
	return argParser.parse_args()

def save_issues(repo_name, issues):
	file_name = f"{repo_name}.txt"
	with open(file_name, "w") as f:
		columns = 'GitHub Issue/PR Title,GitHub Issue/PR URL,Content Source,Product'
		f.write(f"{columns}\n")

		for issue in issues:
			f.write(f"{issue['title']},{issue['url']},{issue['article_url']},{issue['product']}\n")

		print(f"{file_name} successfully generated.")
	
def main():
	print(Fore.GREEN)

	try:
		# Get the command-line args (parameters).
		args = parse_args()

		# Get issues for specified repo.
		gh_issues = get_issues(args.repo)

		issues = []
		for gh_issue in gh_issues:
			issue = build_issue(args.repo, gh_issue)
			issues.append(issue)

		save_issues(args.repo, issues)
	except OSError as error:
		print_error(error)		

	clean_up()
                        
main()
