from github import Github
import os
import urllib.request
import re
import argparse
from colorama import Fore, Back, Style
import pandas as pd
import openpyxl

# Load GitHub application token from environment variable.
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Load Git login ID from environment variable.
GIT_LOGIN = os.environ.get("GIT_LOGIN")

# Load GitHub org name.
GITHUB_ORG = os.getenv('GITHUB_ORG')

# Constants
GITHUB_DOMAIN = 'https://github.com'

def print_error(error_text):
  print(Fore.RED)
  print(f"ERROR:\n{error_text}\n")

def get_issues(org_name, repo_name):
	issues = []

	gh = Github(GITHUB_TOKEN)
	if gh:
		q_repo_name = f"{org_name}/{repo_name}"

		repo = gh.get_repo(q_repo_name)
		if repo:
			issues = repo.get_issues(state='open', assignee=GIT_LOGIN)
	
	return issues

def build_issue(repo_name, gh_issue):
	issue = {}
	issue['title'] = gh_issue.title
	issue['url'] = gh_issue.html_url
	issue['article_url'] = ""
	issue['product'] = ""

	print(f"Reading {gh_issue.html_url}")
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
	argParser.add_argument("-o", "--org", help="GitHub org name.", required=False)
	return argParser.parse_args()

def save_issues_to_excel(repo_name, issues):
	rows = []
	for issue in issues:
		row = [issue['title'], issue['url'], issue['article_url'], issue['product']]
		rows.append(row)

	df = pd.DataFrame(rows,
										index=None,
										columns=['GitHub Issue/PR Title', 'GitHub Issue/PR URL', 'Content Source', 'Product'])
	file_name = f"{repo_name}.xlsx"
	df.to_excel(file_name, sheet_name='GitHub Issues')
	print(f"{file_name} successfully generated.")

def save_issues_to_text(repo_name, issues):
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
		org_name = args.org or GITHUB_ORG
		gh_issues = get_issues(org_name, args.repo)

		issues = []
		for gh_issue in gh_issues:
			issue = build_issue(args.repo, gh_issue)
			issues.append(issue)

		if gh_issues:
			#save_issues_to_text(args.repo, issues)
			save_issues_to_excel(args.repo, issues)
		else:
			print(f"No issues found for {org_name}/{args.repo}")
	except Exception as e:
		print_error(str(e))

	clean_up()
                        
main()
