from github import Github
import os
import urllib.request
import re

token = os.getenv('GITHUB_TOKEN')
gh = Github(token)

github_domain = 'https://github.com'
repo_name = 'MicrosoftDocs/azure-dev-docs'
repo = gh.get_repo(repo_name)

issues = repo.get_issues(state='open', assignee='TomArcherMsft')
with open("test.txt", "w") as f:
	columns = 'GitHub Issue/PR URL,Content Source,Article Focus'
	f.write(f"{columns}\n")

	for issue in issues:
		url = issue.html_url
		response = urllib.request.urlopen(url)
		data = response.read()      # a `bytes` object as data is binary

		content_source_pattern = '<li>Content Source: <a href="(.*?)"'
		matches = re.findall(content_source_pattern, data.decode('utf-8'))
		found_matches = False

		for match in matches:
			found_matches = True

			article_focus = ''
			article_focus_pattern = re.compile(f"{github_domain}/{repo_name}/blob/(main|master)/articles/(.*?)/")
			article_focus_match = article_focus_pattern.search(match)
			if article_focus_match:
				article_focus = article_focus_match.group(2)

			f.write(f"{url},{match},{article_focus}\n")

		if found_matches != True:
			f.write(f"{url},NO MATCHES FOR: {content_source_pattern},UNKNOWN\n")
