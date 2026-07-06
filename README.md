# Curler Manuscript

[![CI](https://github.com/FabianoRaiser/curler-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/FabianoRaiser/curler-cli/actions/workflows/ci.yml)

Curler Manuscript is the first edition of Curler: a tiny command-line browser backed by the system `curl`. It fetches a URL, follows redirects, and prints the raw HTML exactly as the server returned it.

No JavaScript. No HTML parser. No headless browser. Just the document.

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

Fetch a page and print the raw body:

```bash
curler example.com
curler https://example.com
```

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

Start the interactive Manuscript shell:

```bash
curler
```

Inside the REPL:

```text
curler> example.com
curler> headers
curler> raw
curler> pretty
curler> help
curler> quit
```

## Test

Run the unit test suite with the standard library:

```bash
python3 -m unittest discover -s tests
```

## Manual Check

After installing locally, run:

```bash
curler example.com
curler --headers example.com
curler --pretty example.com
curler
```

In the REPL, enter a URL such as `example.com`, then run `headers`, `raw`, `pretty`, and `quit`.

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
git cliff --tag v0.2.0 --prepend CHANGELOG.md
```

On tag push, the [release workflow](.github/workflows/release.yml) runs git-cliff, commits the updated `CHANGELOG.md`, and uses the same output for the GitHub Release notes.

## Roadmap

**Paperback** (next edition) will parse HTML into readable text, numbered links, and REPL navigation (`links`, `go`, `back`, `forward`). See [`docs/curler-guide.md`](docs/curler-guide.md) for the full edition roadmap.

## Limitations

Manuscript does not execute JavaScript, parse HTML into readable text, extract or follow links, keep navigation history, submit forms, send custom headers, or save responses to files. The `--pretty` flag only reindents the markup for reading; it does not interpret the page. Those capabilities belong to later Curler editions.
