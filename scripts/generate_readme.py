import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USERNAME = "SanathBansod"
PROFILE_REPO = USERNAME
README = Path("README.md")
START = "<!-- PROJECTS:START -->"
END = "<!-- PROJECTS:END -->"

API = (
    f"https://api.github.com/users/{urllib.parse.quote(USERNAME)}/repos"
    "?per_page=100&sort=updated&direction=desc&type=owner"
)

def fetch_repositories():
    request = urllib.request.Request(
        API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "SanathBansod-profile-readme-updater",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

def esc(value):
    return (
        str(value or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

def card(repo):
    name = esc(repo["name"])
    description = esc(repo.get("description") or "No description provided.")
    url = repo["html_url"]
    language = esc(repo.get("language") or "Security / Research")
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    updated = repo.get("pushed_at", "")

    if updated:
        dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
        updated_text = dt.astimezone(timezone.utc).strftime("%Y-%m-%d")
    else:
        updated_text = "N/A"

    return f"""<td width=\"50%\" valign=\"top\">

### 🔹 [{name}]({url})

{description}

**Stack:** `{language}`  ·  **⭐** {stars}  ·  **🍴** {forks}  
**Updated:** `{updated_text}`

</td>"""

def build_section(repos):
    repos = [
        r for r in repos
        if not r.get("fork", False)
        and r.get("name", "").lower() != PROFILE_REPO.lower()
        and not r.get("archived", False)
    ]

    if not repos:
        return "> No public projects found yet."

    cells = [card(repo) for repo in repos]
    rows = []
    for i in range(0, len(cells), 2):
        row = cells[i:i+2]
        while len(row) < 2:
            row.append('<td width=\"50%\"></td>')
        rows.append('<tr>\n' + '\n'.join(row) + '\n</tr>')

    return (
        "### 🔄 Latest Public Projects\n\n"
        + '<table>\n' + '\n'.join(rows) + '\n</table>\n'
        + f"\n_Automatically generated from the public repositories of **{USERNAME}**._"
    )

def main():
    text = README.read_text(encoding="utf-8")
    repos = fetch_repositories()
    section = build_section(repos)

    if START not in text or END not in text:
        raise SystemExit("Project markers were not found in README.md.")

    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)

    new_text = before + START + "\n" + section + "\n" + END + after
    README.write_text(new_text, encoding="utf-8")

if __name__ == "__main__":
    main()
