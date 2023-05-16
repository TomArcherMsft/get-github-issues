# Produce a CSV of GitHub Issues

CSV can then be opened in Excel where I can group/filter/sort issues by desired column(s).

## Syntax
`get-github-issues.py [-h] -r REPO`

## Example
`python get-github-issues -r azure-dev-docs`

## Configuration

Create the following environment variables:

| Name | Value |
| GITHUB_TOKEN | Your GitHub Application token |
| GIT_LOGIN | Your Git ID |
| GITHUB_ORG | The org of your repo |

## Additional info

Generated file has following columns:

- GitHub Issue/PR Title
- GitHub Issue/PR URL
- Article URL
- Product/Service
