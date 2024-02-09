import requests
import os

def get_commits_with_label(owner, repo, since_date, until_date, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {
        "since": since_date,
        "until": until_date,
        "per_page": 100,  # ページあたりのコミット数の上限
    }
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"  # GitHubの個人アクセストークン
    }

    commits = []

    while url:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        commits.extend(data)  # 取得したコミット情報をcommitsリストに追加する

        if "next" in response.links:
            url = response.links["next"]["url"]
        else:
            url = None

    return commits


def count_code_changes(commit, token):
    diff_url = commit['url']
    headers = {
        "Accept": "application/vnd.github.diff"
    }
    response = requests.get(diff_url, headers=headers)
    response.raise_for_status()
    diff_content = response.text.splitlines()

    added_lines = sum(1 for line in diff_content if line.startswith('+') and not line.startswith('+++'))
    removed_lines = sum(1 for line in diff_content if line.startswith('-') and not line.startswith('---'))

    return added_lines, removed_lines

# 例: owner = リポジトリの所有者, repo = リポジトリ名, since_date = 開始日, until_date = 終了日, token = GitHubの個人アクセストークン
owner = os.environ.get("GITHUB_OWNER")
repo = os.environ.get("GITHUB_REPO")
since_date = "2023-04-01T00:00:00Z"
until_date = "2024-02-10T23:59:59Z"
token = os.environ.get("GITHUB_TOKEN")

commits = get_commits_with_label(owner, repo, since_date, until_date, token)

for commit in commits:
    print("Commit message:", commit["commit"]["message"])
    # 追加行数や削除行数の処理を追加することができます
    added_lines, removed_lines = count_code_changes(commit, token)
    print("Added lines:", added_lines)
    print("Removed lines:", removed_lines)
    print()