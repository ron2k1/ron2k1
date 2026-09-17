"""Four stat panels. Repo and contribution counts come from the GitHub API; the rest are curated."""
from __future__ import annotations

import argparse
import datetime
import json
import os
import urllib.request

from . import draw as D

W, H, PW, GAP = 880, 140, 202, 24
LABELS = (("public_repos", "PUBLIC REPOS"), ("contributions_past_year", "CONTRIBUTIONS · PAST YEAR"),
          ("hackathon_awards", "HACKATHON AWARDS"), ("ai_roles", "AI ROLES"))
QUERY = """query($login: String!) { user(login: $login) {
  repositories(privacy: PUBLIC, isFork: false, ownerAffiliations: OWNER) { totalCount }
  contributionsCollection { contributionCalendar { totalContributions } } } }"""


def build(values: dict) -> str:
    b = []
    for i, (key, label) in enumerate(LABELS):
        x = 2 + i * (PW + GAP)
        b.append(D.panel(x, 2, PW, 124))
        b.append(D.shadowed_text(x + PW / 2, 78, f"{values[key]:,}", 56, D.RED, [(3, 3, D.INK, 1)], anchor="middle"))
        b.append(f"<text class='m' x='{x + PW / 2}' y='104' font-size='9' font-weight='500' letter-spacing='.14em' "
                 f"text-anchor='middle' fill='{D.INKSOFT}'>{label}</text>")
    label = ", ".join(f"{values[k]:,} {lbl.lower().replace(' · ', ' in the ')}" for k, lbl in LABELS)
    return D.svg(W, H, label, "".join(b))


def fetch(login: str, token: str | None) -> dict | None:
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body,
                                 headers={"Content-Type": "application/json", "User-Agent": "ron2k1-profile"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            user = json.load(r)["data"]["user"]
        return {"public_repos": user["repositories"]["totalCount"],
                "contributions_past_year": user["contributionsCollection"]["contributionCalendar"]["totalContributions"]}
    except Exception as err:  # keep the old numbers on any failure, never invent
        print(f"stats fetch failed: {type(err).__name__}")
        return None


def merge(old: dict, fresh: dict | None) -> dict:
    out = dict(old)
    if fresh:
        out.update(fresh)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", default="ron2k1")
    ap.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    path = D.ROOT / "data" / "stats.json"
    old = json.loads(path.read_text(encoding="utf-8"))
    fresh = None if a.offline else fetch(a.login, a.token)
    values = merge(old, fresh)
    if fresh:
        values["fetched_at"] = datetime.date.today().isoformat()
    path.write_text(json.dumps(values, indent=2) + "\n", encoding="utf-8")
    D.write(D.ROOT / "assets" / "stats.svg", build(values))
    print("assets/stats.svg written", values)
