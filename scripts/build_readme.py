#!/usr/bin/env python3
"""Generate README.md from catalog.json and validate it against the PDFs tracked by git.

Usage:
    scripts/build_readme.py           # rewrite README.md
    scripts/build_readme.py --check   # exit 1 if README.md is stale or the catalog is inconsistent
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"
README = ROOT / "README.md"
FILENAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*-\d{4}\.pdf$")

HEADER = """# Bookshelf

Technical books and articles I have read. Each PDF is committed once read.

> Generated from `catalog.json` by `scripts/build_readme.py`. Do not edit by hand.

## Adding a book

1. Name the PDF `<first-author-surname>-<title-in-kebab-case>-<year>.pdf`
   (lowercase ASCII, digits and dashes only), e.g. `martin-the-clean-coder-2011.pdf`.
2. Add an entry to `catalog.json` (`file`, `title`, `authors`, `year`, `url`, optional `articles`
   as a list of `{"title": ..., "url": ...}`).
3. `git add` both and commit: the pre-commit hook regenerates and stages this README.
   CI fails if the README, the catalog and the committed PDFs ever disagree.

One-time setup per clone: `git config core.hooksPath .githooks`
"""


def tracked_pdfs() -> set[str]:
    out = subprocess.run(
        ["git", "ls-files", "--", "*.pdf"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout
    return set(out.splitlines())


def validate(entries: list[dict]) -> list[str]:
    errors = []
    files = [e["file"] for e in entries]
    for name in files:
        if not FILENAME_RE.match(name):
            errors.append(f"bad file name (expected author-title-year.pdf): {name}")
    duplicates = {f for f in files if files.count(f) > 1}
    errors += [f"duplicate catalog entry: {f}" for f in sorted(duplicates)]
    tracked = tracked_pdfs()
    errors += [f"PDF tracked by git but missing from catalog.json: {f}" for f in sorted(tracked - set(files))]
    errors += [f"catalog.json entry whose PDF is not tracked by git: {f}" for f in sorted(set(files) - tracked)]
    for e in entries:
        for key in ("title", "authors", "year", "url"):
            if not e.get(key):
                errors.append(f"{e['file']}: missing '{key}'")
    return errors


def render(entries: list[dict]) -> str:
    entries = sorted(entries, key=lambda e: e["title"].lower())
    lines = [HEADER, f"## Books ({len(entries)})", ""]
    lines += ["| Title | Author(s) | Year | Links |", "| --- | --- | --- | --- |"]
    for e in entries:
        links = [f"[PDF]({quote(e['file'])})", f"[Book page]({e['url']})"]
        links += [f"[{a['title']}]({a['url']})" for a in e.get("articles", [])]
        lines.append(f"| {e['title']} | {', '.join(e['authors'])} | {e['year']} | {' · '.join(links)} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    entries = json.loads(CATALOG.read_text())
    errors = validate(entries)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    content = render(entries)
    if "--check" in sys.argv:
        if not README.exists() or README.read_text() != content:
            print("README.md is stale: run scripts/build_readme.py", file=sys.stderr)
            return 1
        return 0
    README.write_text(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
