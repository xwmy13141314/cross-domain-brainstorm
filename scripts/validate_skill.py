#!/usr/bin/env python3
"""Validate the cross-domain-brainstorm skill package.

Pure standard library. Checks:
- required files and SKILL.md frontmatter
- references and relative markdown links
- domain deck schema (48 unique domains, valid axes)
- every domain appears in references/domain-library.md
- eval cases count
- markdown table column consistency
- domain sampler self-test
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AXES = {
    "substrate": {"physical", "digital", "social", "biological", "institutional"},
    "centralization": {"centralized", "distributed", "networked"},
    "sync": {"realtime", "batch", "long_cycle", "episodic"},
    "risk": {"low", "medium", "high", "irreversible"},
    "resource": {"abundant", "scarce", "volatile"},
    "verification": {"external", "self_reported", "none"},
    "agent": {"individual", "team", "crowd", "algorithm", "mixed"},
}
RICHNESS = {"high", "medium", "low"}
REQUIRED = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "CONTRIBUTING.md",
    ".gitignore",
    ".markdownlint.json",
    ".markdownlintignore",
    ".github/workflows/ci.yml",
    "references/domain-library.md",
    "references/mechanism-examples.md",
    "references/grafting.md",
    "references/convergence.md",
    "references/red-team.md",
    "references/facilitation.md",
    "references/output-templates.md",
    "references/example-session.md",
    "references/example-session-hardware.md",
    "assets/domain-deck.json",
    "scripts/domain_sampler.py",
    "scripts/validate_skill.py",
    "scripts/package.ps1",
    "evals/cases.md",
    "evals/rubric.md",
    "evals/run.md",
]
LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(([^)]+)\)")
REF_RE = re.compile(r"references/[A-Za-z0-9._-]+\.md")
SKIP_DIRS = {".git", ".npm-cache", "node_modules", ".venv", "venv"}


def markdown_files():
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required() -> None:
    missing = [rel for rel in REQUIRED if not (ROOT / rel).exists()]
    if missing:
        fail(f"missing required files: {', '.join(missing)}")
    print(f"OK required files ({len(REQUIRED)})")


def check_frontmatter() -> None:
    text = read(ROOT / "SKILL.md")
    if not text.startswith("---"):
        fail("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        fail("SKILL.md frontmatter is not closed")
    front = text[3:end]
    for key in ("name:", "description:", "version:"):
        if key not in front:
            fail(f"SKILL.md frontmatter missing {key}")
    if "cross-domain-brainstorm" not in front:
        fail("SKILL.md name must be cross-domain-brainstorm")
    if "version: 0.2.0" not in front:
        fail("SKILL.md frontmatter version must be 0.2.0")
    print("OK SKILL.md frontmatter")


def check_references() -> None:
    text = read(ROOT / "SKILL.md")
    refs = sorted(set(REF_RE.findall(text)))
    if len(refs) < 8:
        fail(f"SKILL.md should reference at least 8 reference files, found {len(refs)}")
    missing = [ref for ref in refs if not (ROOT / ref).exists()]
    if missing:
        fail(f"SKILL.md references missing files: {', '.join(missing)}")
    print(f"OK SKILL.md references ({len(refs)})")


def check_links() -> None:
    problems = []
    for path in markdown_files():
        text = read(path)
        for _, target in LINK_RE.findall(text):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if not resolved.exists():
                problems.append(f"{path.relative_to(ROOT)} -> {target}")
    if problems:
        fail("broken relative links:\n  " + "\n  ".join(problems))
    print("OK relative markdown links")


def check_deck() -> dict:
    deck_path = ROOT / "assets/domain-deck.json"
    try:
        deck = json.loads(read(deck_path))
    except json.JSONDecodeError as exc:
        fail(f"domain-deck.json is not valid JSON: {exc}")
    domains = deck.get("domains", [])
    if len(domains) != 48:
        fail(f"expected 48 domains, found {len(domains)}")
    ids, names = set(), set()
    for domain in domains:
        for key in ("id", "name", "family", "axes", "mechanisms", "richness"):
            if key not in domain:
                fail(f"domain missing {key}: {domain.get('id', '?')}")
        if domain["id"] in ids or domain["name"] in names:
            fail(f"duplicate domain: {domain['id']} / {domain['name']}")
        ids.add(domain["id"])
        names.add(domain["name"])
        if domain["richness"] not in RICHNESS:
            fail(f"bad richness: {domain['id']} -> {domain['richness']}")
        for axis, allowed in AXES.items():
            value = domain["axes"].get(axis)
            if value not in allowed:
                fail(f"bad axis {axis}={value!r} for {domain['id']}")
    print(f"OK domain deck ({len(domains)} domains)")
    return deck


def check_domain_library(deck: dict) -> None:
    text = read(ROOT / "references/domain-library.md")
    missing = [domain["name"] for domain in deck["domains"] if domain["name"] not in text]
    if missing:
        fail(f"domain-library.md missing domain names: {', '.join(missing)}")
    print(f"OK domain-library names ({len(deck['domains'])})")


def check_evals() -> None:
    text = read(ROOT / "evals/cases.md")
    count = len(re.findall(r"^## Case \d+", text, flags=re.MULTILINE))
    if count < 6:
        fail(f"evals/cases.md should contain at least 6 cases, found {count}")
    for name in ("rubric.md", "run.md"):
        if not (ROOT / "evals" / name).exists():
            fail(f"missing evals/{name}")
    print(f"OK eval cases ({count})")


def check_tables() -> None:
    problems = []
    for path in markdown_files():
        lines = read(path).splitlines()
        in_code = False
        block = []
        start = 0
        counts = []

        def flush() -> None:
            nonlocal block, counts
            if block and len(set(counts)) > 1:
                problems.append(
                    f"{path.relative_to(ROOT)}:{start}-{start + len(block) - 1} "
                    f"table columns {sorted(set(counts))}"
                )
            block, counts = [], []

        for index, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("```"):
                flush()
                in_code = not in_code
                continue
            if in_code:
                continue
            if stripped.startswith("|"):
                if not block:
                    start = index
                block.append(line)
                counts.append(line.count("|"))
            else:
                flush()
        flush()
    if problems:
        fail("markdown table column mismatches:\n  " + "\n  ".join(problems))
    print("OK markdown tables")


def check_sampler() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/domain_sampler.py"), "--self-test"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        fail(f"domain_sampler self-test failed:\n{result.stdout}\n{result.stderr}")
    print(result.stdout.strip())
    print("OK domain sampler self-test")


def main() -> int:
    print(f"Validating {ROOT}")
    check_required()
    check_frontmatter()
    check_references()
    check_links()
    deck = check_deck()
    check_domain_library(deck)
    check_evals()
    check_tables()
    check_sampler()
    print("VALIDATION OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
