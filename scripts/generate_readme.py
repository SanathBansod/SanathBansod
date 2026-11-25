import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USERNAME = "SanathBansod"
PROFILE_REPO = USERNAME
README = Path("README.md")
START = "<!-- PROJECTS:START -->"
END = "<!-- PROJECTS:END -->"
ANCHOR = "## 🧪 How I Approach a Lab"

API = (
    f"https://api.github.com/users/{urllib.parse.quote(USERNAME)}/repos"
    "?per_page=100&sort=updated&direction=desc&type=owner"
)


def fetch_repositories():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "SanathBansod-profile-readme-updater",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(API, headers=headers)
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

    return f"""<td width="50%" valign="top">

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
    # Keep the profile showcase focused on the newest public work.
    # Older projects remain documented in the manually curated section above.
    repos = repos[:8]

    if not repos:
        return "> No public projects found yet."

    cells = [card(repo) for repo in repos]
    rows = []
    for i in range(0, len(cells), 2):
        row = cells[i:i + 2]
        while len(row) < 2:
            row.append('<td width="50%"></td>')
        rows.append("<tr>\n" + "\n".join(row) + "\n</tr>")

    return (
        "### 🔄 Latest Public Projects\n\n"
        + "<table>\n" + "\n".join(rows) + "\n</table>\n"
        + f"\n_Automatically generated from the public repositories of **{USERNAME}**._"
    )


def update_readme(text, section):
    # Replace the generated block on subsequent runs.
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        return before + START + "\n" + section + "\n" + END + after

    # On the first run, add the block before the existing lab-methodology section.
    # This preserves the manually curated project catalogue in the README.
    if ANCHOR not in text:
        raise SystemExit(
            f"Could not find either project markers or the insertion heading: {ANCHOR}"
        )

    block = f"{START}\n{section}\n{END}\n\n"
    return text.replace(ANCHOR, block + ANCHOR, 1)


def main():
    text = README.read_text(encoding="utf-8")
    repos = fetch_repositories()
    section = build_section(repos)
    new_text = update_readme(text, section)

    if new_text != text:
        README.write_text(new_text, encoding="utf-8")
        print("README project section updated successfully.")
    else:
        print("README is already up to date.")


if __name__ == "__main__":
    main()
