# Curler Manuscript

![CI](https://github.com/FabianoRaiser/curler-cli/actions/workflows/ci.yml/badge.svg)

Curler Manuscript is the first edition of Curler: a tiny command-line browser backed by the system `curl`. It fetches a URL, follows redirects, and prints the raw HTML exactly as the server returned it.

No JavaScript. No HTML parser. No headless browser. Just the document.

## Requirements

- Python 3.10+
- `curl` installed and available on `PATH`

## Install

Create a virtual environment (recommended on Debian/Ubuntu to avoid PEP 668 errors):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

If you rename or move the project folder, recreate `.venv` from scratch — virtualenv paths are not portable.

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

Install dev tools inside your virtualenv:

```bash
pip install pre-commit ruff
pre-commit install
pre-commit run --all-files
```

## Roadmap

**Paperback** (next edition) will parse HTML into readable text, numbered links, and REPL navigation (`links`, `go`, `back`, `forward`). See [`docs/curler-guide.md`](docs/curler-guide.md) for the full edition roadmap.

## Limitations

Manuscript does not execute JavaScript, parse HTML into readable text, extract or follow links, keep navigation history, submit forms, send custom headers, or save responses to files. The `--pretty` flag only reindents the markup for reading; it does not interpret the page. Those capabilities belong to later Curler editions.
