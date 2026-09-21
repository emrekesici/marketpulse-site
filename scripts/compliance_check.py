#!/usr/bin/env python3
"""
Pre-publish compliance scan for the published site.

Encodes the hard rules from .claude/skills/marketpulse/SKILL.md and the content
standard in docs/BRD.md §7 so they are enforced mechanically rather than
remembered. Runs in CI before the Pages upload; exits non-zero on any violation.

editions.json and data.json are served alongside index.html, and the archive
carries every past edition's wording forward, so scanning the rendered page
alone would miss most of it. Kept in sync with the copy in the private source
repo — change both together.

    python scripts/compliance_check.py [--quiet]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT  # published output lives at the repo root here

# Naming the employer is out of scope for deployed content (BRD §4.4, §7).
EMPLOYER_PATTERNS = [
    (r"\bBoA\b", "names the employer"),
    (r"\bBofA\b", "names the employer"),
    (r"Bank of America", "names the employer"),
    (r"\bBAC\b", "the employer's ticker — do not feature it, even to exclude it"),
    (r"OBA policy", "discloses the employment relationship"),
    (r"\(employer\)", "discloses the employment relationship"),
    (r"my employer|the founder's employer", "discloses the employment relationship"),
]
# Job-title references (BRD §7). Deliberately narrow to avoid false hits on
# ordinary market copy such as "bank earnings" or "a senior analyst said".
TITLE_PATTERNS = [
    (r"senior officer", "job-title reference"),
    (r"\bI work at\b|\bI'm employed\b", "employment reference"),
]

SCAN_FILES = ["index.html", "template.html", "editions.json", "data.json"]


def scan_text(path: Path) -> list[str]:
    text = path.read_text(errors="replace")
    found = []
    for pat, why in EMPLOYER_PATTERNS + TITLE_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            line = text.count("\n", 0, m.start()) + 1
            ctx = re.sub(r"\s+", " ", text[max(0, m.start() - 55): m.end() + 55])
            found.append(f"{path.relative_to(ROOT)}:{line}  {why}\n      …{ctx}…")
    return found


def scan_editions() -> list[str]:
    """Rules that need the parsed edition rather than raw text."""
    problems = []
    path = SITE / "editions.json"
    if not path.exists():
        return [f"{path.relative_to(ROOT)} is missing"]
    for e in json.loads(path.read_text()):
        d = e.get("date", "?")
        action = e.get("action", "")
        if not re.search(r"not financial advice", action, re.I):
            problems.append(f"edition {d}: action plan has no not-financial-advice line (SKILL hard rule 3)")
        if not re.search(r"hypothetical|model illustration|model book|informational", action, re.I):
            problems.append(f"edition {d}: action plan does not label the portfolio as hypothetical")
        scen = e.get("scenarios", [])
        if len(scen) != 3:
            problems.append(f"edition {d}: expected 3 scenarios, found {len(scen)}")
        elif abs(sum(s[0] for s in scen) - 100) > 1:
            problems.append(f"edition {d}: scenario probabilities sum to {sum(s[0] for s in scen)}, not 100")
    return problems


def main() -> int:
    quiet = "--quiet" in sys.argv
    problems: list[str] = []
    for name in SCAN_FILES:
        p = SITE / name
        if p.exists():
            problems.extend(scan_text(p))
        elif name in ("index.html", "editions.json"):
            problems.append(f"site/{name} is missing")
    problems.extend(scan_editions())

    if problems:
        print("COMPLIANCE CHECK: FAIL\n", file=sys.stderr)
        for p in problems:
            print(f"  · {p}", file=sys.stderr)
        print(
            f"\n{len(problems)} issue(s). Publishing is blocked until these are resolved"
            "\n(docs/BRD.md §7, docs/SECRETS.md §4).",
            file=sys.stderr,
        )
        return 1
    if not quiet:
        print(f"COMPLIANCE CHECK: PASS — {len(SCAN_FILES)} files scanned, no employer or title references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
