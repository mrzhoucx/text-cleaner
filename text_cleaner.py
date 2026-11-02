#!/usr/bin/env python3
"""Clean text files: strip trailing whitespace, normalize line endings,
and collapse runs of blank lines. Zero dependencies.

Usage:
    python3 text_cleaner.py file.txt [--in-place] [--check]
    python3 text_cleaner.py file1.txt file2.txt --max-blank 2
    cat file.txt | python3 text_cleaner.py

Without --in-place, cleaned text goes to stdout (one file at a time).
With --check, nothing is written; exit code 1 if any file would change.
"""
import argparse
import sys


def clean_text(text, max_blank=1):
    """Return (cleaned_text, stats dict)."""
    # Normalize CRLF / CR to LF first, so trailing-whitespace stripping
    # and blank-line collapsing work on a single line-ending style.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    # A trailing newline produces a final empty element; drop it here and
    # re-add exactly one newline at the end if the input was non-empty.
    had_trailing_newline = text.endswith("\n")
    if had_trailing_newline and lines and lines[-1] == "":
        lines.pop()
    trimmed = 0
    blank_removed = 0
    out = []
    blank_run = 0
    for line in lines:
        stripped = line.rstrip(" \t")
        if stripped != line:
            trimmed += 1
        if stripped == "":
            blank_run += 1
            if blank_run > max_blank:
                blank_removed += 1
                continue
        else:
            blank_run = 0
        out.append(stripped)
    # Drop leading blank lines; they are never meaningful in a cleaned file.
    while out and out[0] == "":
        out.pop(0)
        blank_removed += 1
    # Drop trailing blank lines; the final newline below is the terminator.
    while out and out[-1] == "":
        out.pop()
        blank_removed += 1
    result = "\n".join(out)
    if result:
        result += "\n"
    return result, {"lines_trimmed": trimmed,
                    "blank_lines_removed": blank_removed}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("files", nargs="*", help="Text files to clean (default: stdin)")
    parser.add_argument("--in-place", action="store_true",
                        help="Rewrite each file instead of printing to stdout")
    parser.add_argument("--check", action="store_true",
                        help="Exit 1 if any file would change; write nothing")
    parser.add_argument("--max-blank", type=int, default=1,
                        help="Max consecutive blank lines to keep (default: 1)")
    args = parser.parse_args(argv)
    if args.max_blank < 0:
        parser.error("--max-blank must be >= 0")

    if not args.files:
        if args.in_place or args.check:
            parser.error("--in-place/--check need at least one file")
        original = sys.stdin.read()
        cleaned, _ = clean_text(original, args.max_blank)
        sys.stdout.write(cleaned)
        return 0

    would_change = False
    for path in args.files:
        try:
            with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
                original = f.read()
        except OSError as exc:
            print(f"text_cleaner: {path}: {exc}", file=sys.stderr)
            return 2
        cleaned, stats = clean_text(original, args.max_blank)
        if cleaned != original:
            would_change = True
        if args.check:
            status = "would change" if cleaned != original else "clean"
            print(f"{path}: {status} ({stats['lines_trimmed']} lines trimmed)")
        elif args.in_place:
            if cleaned != original:
                with open(path, "w", encoding="utf-8", errors="surrogateescape") as f:
                    f.write(cleaned)
            print(f"{path}: {'updated' if cleaned != original else 'unchanged'}")
        else:
            sys.stdout.write(cleaned)
    return 1 if (args.check and would_change) else 0


if __name__ == "__main__":
    raise SystemExit(main())
