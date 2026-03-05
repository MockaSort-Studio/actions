"""
Match a list of changed file paths against glob patterns.

Reads from environment:
  CHANGED_FILES — JSON array of file paths
  PATTERNS      — newline-separated glob patterns

Glob semantics:
  **   matches any characters across path segments
  *    matches any characters within a single segment
  ?    matches one character within a single segment
  /    trailing slash matches the folder prefix and anything inside it

Exits 0 and prints "true" if any file matches any pattern, else prints "false".
"""

import os
import re
import json
import sys


def to_regex(pattern: str) -> re.Pattern:
    if pattern.endswith("/"):
        # folder prefix — match the folder itself or anything inside it
        return re.compile("^" + re.escape(pattern))
    # re.escape first, then restore glob wildcard semantics
    p = re.escape(pattern)
    p = p.replace(r"\*\*", ".*")    # ** → any depth
    p = p.replace(r"\*", "[^/]*")   # *  → within one segment
    p = p.replace(r"\?", "[^/]")    # ?  → one char within a segment
    return re.compile("^" + p + "$")


def main() -> None:
    raw = os.environ.get("CHANGED_FILES", "[]")
    try:
        files = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"error: CHANGED_FILES is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(2)

    patterns = [
        p.strip()
        for p in os.environ.get("PATTERNS", "").strip().splitlines()
        if p.strip()
    ]

    if not patterns:
        print("false")
        return

    regexes = [to_regex(p) for p in patterns]
    matched = any(rx.search(f) for f in files for rx in regexes)
    print("true" if matched else "false")


if __name__ == "__main__":
    main()
