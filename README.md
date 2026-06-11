# Curler Manuscript

Curler Manuscript is the first edition of Curler: a tiny command-line browser backed by the system `curl`. It fetches a URL, follows redirects, and prints the raw HTML exactly as the server returned it.

No JavaScript. No HTML parser. No pretty output. Just the document.

## Requirements

- Python 3.10+
- `curl` installed and available on `PATH`
- `pip`

## Install

```bash
pip install -e .
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

Print response headers followed by the raw body:

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
curler
```

In the REPL, enter a URL such as `example.com`, then run `headers`, `raw`, `pretty`, and `quit`.

## Limitations

Manuscript does not execute JavaScript, extract links, keep navigation history, submit forms, send custom headers, or save responses to files. The `--pretty` view only reindents the markup for reading; it does not interpret the page like Paperback will. Those belong to later Curler editions.
