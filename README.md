# Curler Paperback

[![CI](https://github.com/FabianoRaiser/curler-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/FabianoRaiser/curler-cli/actions/workflows/ci.yml)

Curler Paperback is the second edition of Curler: a command-line browser backed by the system `curl`. It fetches a URL, follows redirects, parses the HTML, and prints a readable page with title, text, and inline link references (`[1]`, `[2]`, …). Run `links` in the REPL to see full URLs.

No JavaScript. No headless browser. Just the document — interpreted enough to read and navigate.

## Requirements

- Python 3.10+
- `curl` installed and available on `PATH`

## Install

Use a virtual environment — on Debian/Ubuntu the system Python is **externally managed** (PEP 668), so `pip install` without venv fails with `externally-managed-environment`.

```bash
# clone and enter the repo
git clone https://github.com/FabianoRaiser/curler-cli.git
cd curler-cli

# create and activate a venv (once per machine / folder)
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# install the CLI in editable mode
pip install -e .
```

If `python3 -m venv .venv` fails, install the venv module first:

```bash
sudo apt install python3-venv python3-full
```

**Check that the venv is active** before installing or running tests:

```bash
which python   # should end with .venv/bin/python
which pip      # should end with .venv/bin/pip
```

**After renaming or moving the project folder**, delete `.venv` and recreate it — paths inside the venv are absolute and break when the directory changes.

For development tools (pre-commit, Ruff, build):

```bash
pip install -e ".[dev]"
```

## Use

Fetch a page and print a readable parsed view (default):

```bash
curler example.com
curler https://example.com
```

Print the raw HTML body (Manuscript-style):

```bash
curler --raw example.com
```

Disable ANSI colors in parsed output:

```bash
curler --no-color example.com
```

Also respects the `NO_COLOR` environment variable.

Send custom request headers (repeatable; curl-style `-H`):

```bash
curler -H 'Accept: application/json' example.com
curler -H 'Accept: application/json' -H 'X-Debug: 1' example.com
```
`--header`/`-H` adds headers to the request. Do not confuse with `--headers`, which prints response headers.

Send or save cookies (curl-style `-b`/`-c`). Cookies are stored only in the file you pass - there is no default jar yet:

```bash
# write cookies received from the response
curler --cookie-jar ./jar.txt example.com

# send cookies from a file (or NAME=VALUE string)
curler --cookie ./jar.txt example.com
curler --cookie 'session=abc123' example.com

# both: reuse and update the same jar across requests
curler --cookie ./jar.txt --cookie-jar ./jar.txt example.com
```
`-b`/`--cookie` sends cookies; `-c`/`--cookie-jar` writes them. Use the same file for both when you want a session between fetches.

Print only response headers:

```bash
curler --headers example.com
```

Print response headers followed by the body:

```bash
curler --include-headers example.com
```

Print the body with readable HTML indentation:

```bash
curler --pretty example.com
```

Start the interactive Paperback shell:

```bash
curler
```

Inside the REPL:

```text
curler> example.com
curler> links
curler> go 1
curler> back
curler> forward
curler> headers
curler> raw
curler> pretty
curler> help
curler> quit
```

### Parsed output

- Headings appear as `#`, `##`, etc.
- Links appear inline as `text [1]`; run `links` in the REPL for full URLs
- Footer shows link count: `(N links)` or `(N links — use links)` in the REPL
- ANSI colors in interactive terminals; use `--no-color` or pipe to disable

## Test

Run the unit test suite with the standard library:

```bash
python3 -m unittest discover -s tests
```

## Manual Check

After installing locally, run:

```bash
curler example.com
curler --raw example.com
curler -H 'Accept: application/json' example.com
curler --headers example.com
curler --pretty example.com
curler --cookie-jar ./jar.txt example.com
curler --cookie ./jar.txt example.com
curler
```

In the REPL, enter a URL such as `example.com`, then run `links`, `go 1`, `back`, `headers`, `raw`, and `quit`.

## Development

With the venv activated and dev extras installed (`pip install -e ".[dev]"`):

```bash
pre-commit install
pre-commit run --all-files
python3 -m unittest discover -s tests
```

### Changelog

We follow [Keep a Changelog](https://keepachangelog.com/). The `[0.1.0]` section was written manually; from `v0.2.0` onward, release sections are generated with [git-cliff](https://git-cliff.org) from Conventional Commits.

Preview unreleased changes (since the last tag):

```bash
git cliff --unreleased
```

Generate a release section locally (does not overwrite `[0.1.0]` — use `--prepend`):

```bash
git cliff --latest --tag v0.2.2 --prepend CHANGELOG.md
```

Commit the updated `CHANGELOG.md` before tagging. On tag push, the [release workflow](.github/workflows/release.yml) runs git-cliff for the GitHub Release notes only (no repo commit — tag checkout is detached HEAD).

## Roadmap

**Hardbound** (next edition) deepens curl — custom request headers, POST body, save, timeout/User-Agent — without a headless browser. See [`docs/curler-guide.md`](docs/curler-guide.md) for the edition roadmap.

## Limitations

Paperback does not execute JavaScript. Client-rendered SPAs often return an empty shell — Curler detects this and warns you; that case stays out of scope (curl shows the HTTP document, not a JS runtime). It does not yet submit forms or save responses to files — those belong to Hardbound. Custom request headers (`-H` / `--header`) and cookies (`-b`/`--cookie`, `-c`/`--cookie-jar`) are already supported.
