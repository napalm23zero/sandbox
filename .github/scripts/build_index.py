"""Validate the repo layout and rebuild the index table in README.md.

Usage: python3 .github/scripts/build_index.py [--check]

--check fails instead of writing when README.md is out of date (CI mode).
"""
import re
import sys
from pathlib import Path

CATEGORIES = {"00-notes": "Notes", "01-snippets": "Snippets", "02-labs": "Labs", "03-challenges": "Challenges"}
STATUSES = ("backlog", "learning", "practicing", "comfortable")
DOMAINS = ("languages", "backend", "frontend", "data", "devops", "cloud", "security", "architecture", "fundamentals", "ai")
ENTRY = re.compile(r"^(\d{2})-[a-z0-9]+(-[a-z0-9]+)*$")
AREA = re.compile(r"^@[a-z]+(-[a-z]+)*$")
START, END = "<!-- index:start -->", "<!-- index:end -->"


class LayoutError(Exception):
    pass


def read_tech(tech):
    readme = tech / "README.md"
    if not readme.is_file():
        raise LayoutError(f"{tech.name}: missing README.md")
    text = readme.read_text()
    frontmatter = re.match(r"---\n(.*?)\n---\n", text, re.S)
    title = re.search(r"^# (.+)$", text, re.M)
    if not frontmatter or not title:
        raise LayoutError(f"{tech.name}/README.md: needs frontmatter and a '# ' title")
    meta = dict(line.split(": ", 1) for line in frontmatter.group(1).splitlines())
    if meta.get("domain") not in DOMAINS:
        raise LayoutError(f"{tech.name}: domain must be one of {DOMAINS}")
    if meta.get("status") not in STATUSES:
        raise LayoutError(f"{tech.name}: status must be one of {STATUSES}")
    return title.group(1), meta


def count_entries(category):
    numbers = set()
    for entry in category.iterdir():
        if entry.name.startswith("."):
            continue
        is_note = category.name == "00-notes"
        name = entry.stem if is_note else entry.name
        match = ENTRY.match(name)
        if not match or entry.is_dir() == is_note or (is_note and entry.suffix != ".md"):
            kind = "a NN-kebab-case.md file" if is_note else "a NN-kebab-case folder"
            raise LayoutError(f"{category.parent.name}/{category.name}/{entry.name}: must be {kind}")
        if match.group(1) in numbers:
            raise LayoutError(f"{category.parent.name}/{category.name}: number {match.group(1)} used twice")
        numbers.add(match.group(1))
    return len(numbers)


def visible_dirs(path):
    return sorted(p for p in path.iterdir() if p.is_dir() and not p.name.startswith("."))


def build_sections(root):
    sections = {}
    for area in visible_dirs(root):
        if not AREA.match(area.name):
            raise LayoutError(f"{area.name}: top-level content lives in areas named like @tech")
        sections[area.name] = build_rows(area)
    return sections


def build_rows(area):
    rows = []
    for tech in visible_dirs(area):
        title, meta = read_tech(tech)
        counts = dict.fromkeys(CATEGORIES, 0)
        for child in tech.iterdir():
            if child.name == "README.md" or child.name.startswith("."):
                continue
            if child.name not in CATEGORIES:
                raise LayoutError(f"{tech.name}/{child.name}: allowed entries are README.md and {list(CATEGORIES)}")
            counts[child.name] = count_entries(child)
        rows.append((meta["domain"], title, f"{area.name}/{tech.name}", meta["status"], *counts.values()))
    return sorted(rows, key=lambda row: (DOMAINS.index(row[0]), row[1].lower()))


def render_table(rows):
    lines = ["| Domain | Subject | Status | " + " | ".join(CATEGORIES.values()) + " |", "|---" * (3 + len(CATEGORIES)) + "|"]
    for domain, title, folder, status, *counts in rows:
        lines.append(f"| {domain} | [{title}]({folder}/) | {status} | " + " | ".join(map(str, counts)) + " |")
    return "\n".join(lines)


def render(sections):
    return "\n\n".join(f"### {area}\n\n{render_table(rows)}" for area, rows in sections.items())


def rebuild(readme_text, sections):
    before, rest = readme_text.split(START, 1)
    _, after = rest.split(END, 1)
    return f"{before}{START}\n{render(sections)}\n{END}{after}"


def main():
    root = Path(__file__).resolve().parents[2]
    readme = root / "README.md"
    try:
        sections = build_sections(root)
    except LayoutError as error:
        sys.exit(f"layout: {error}")
    current = readme.read_text()
    updated = rebuild(current, sections)
    if "--check" in sys.argv:
        if updated != current:
            sys.exit("README.md index is stale: run python3 .github/scripts/build_index.py")
        return
    readme.write_text(updated)


if __name__ == "__main__":
    main()
