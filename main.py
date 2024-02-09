import requests

def get_commits_with_label(owner, repo, label, since_date, until_date, token):
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

        for commit in data:
            if label in commit["commit"]["message"]:
                commits.append(commit)

        if "next" in response.links:
            url = response.links["next"]["url"]
        else:
            url = None

    return commits

# 例: owner = リポジトリの所有者, repo = リポジトリ名, label = ラベル名, since_date = 開始日, until_date = 終了日, token = GitHubの個人アクセストークン
owner = "leexei"
repo = "github_code_measure"
label = "label_name"
since_date = "2023-04-01T00:00:00Z"
until_date = "2024-02-09T23:59:59Z"
token = ""

commits = get_commits_with_label(owner, repo, label, since_date, until_date, token)

for commit in commits:
    print(commit["commit"]["message"])
    # 追加行数や削除行数の処理を追加することができます
