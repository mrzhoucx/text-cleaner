# text-cleaner

Clean text files: strip trailing whitespace, normalize CRLF/CR line endings to LF, and collapse runs of blank lines. Zero dependencies, Python 3 only — handy for tidying notes, configs, and pasted text on a VPS.

## Install

No install needed. Just download `text_cleaner.py`:

```sh
curl -O https://raw.githubusercontent.com/mrzhoucx/text-cleaner/main/text_cleaner.py
chmod +x text_cleaner.py
```

Requires Python 3.8+.

## Usage

Print the cleaned text to stdout (original file untouched):

```sh
python3 text_cleaner.py notes.txt
```

Rewrite the file in place:

```sh
python3 text_cleaner.py notes.txt --in-place
```

Check whether files would change, without writing anything (exit 1 if any would change — useful in a script or pre-commit check):

```sh
python3 text_cleaner.py notes.txt --check
```

Read from stdin:

```sh
cat notes.txt | python3 text_cleaner.py
```

Keep up to 2 consecutive blank lines instead of the default 1:

```sh
python3 text_cleaner.py notes.txt --max-blank 2
```

## Example

Input:

```
hello world␣␣␣
␍␊
␍␊
␍␊
second line␉
```

Output:

```
hello world

second line
```

## Options

| Option | Meaning |
| --- | --- |
| `--in-place` | Rewrite each file instead of printing to stdout |
| `--check` | Report only; exit 1 if any file would change |
| `--max-blank N` | Max consecutive blank lines to keep (default: 1) |
