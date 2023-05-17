# Get GitHub Issues and save in Excel file

File can then be opened in Excel where you can group/filter/sort issues by desired column(s).

## Syntax

`get-github-issues.py [-h] -r REPO [-o ORG]`

**Key points:**
- The GitHub org can be specified as an [environment variable](#configuration) or on the command line. (The command-line value overrides the environment-variable value.)

## Example

`python get-github-issues -r terraform -o azure`

## Configuration

Create the following environment variables:

| Name         | Description                                                                |
|--------------|----------------------------------------------------------------------------|
| GITHUB_TOKEN | Your GitHub Application token.                                             |
| GIT_LOGIN    | Your Git ID.                                                               |
| GITHUB_ORG   | The org of your repo. Can be overridden with the -o command-line argument. |

## Additional info

Generated file has following columns:

- GitHub Issue/PR Title
- GitHub Issue/PR URL
- Article URL
- Product/Service
