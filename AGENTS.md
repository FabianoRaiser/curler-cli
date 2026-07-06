# Curler Paperback

CLI que busca URLs via `curl`, parseia HTML com BeautifulSoup e imprime páginas legíveis no terminal. Edição **Paperback** (v0.2): links inline, navegação REPL, cores ANSI.

## Stack

- Python 3.10+
- `curl` no `PATH`
- `beautifulsoup4`, `lxml`
- `unittest` + `ruff` (dev)

## Comandos

- Instalar: `pip install -e .`
- Dev: `pip install -e ".[dev]"`
- Testes: `python -m unittest discover -s tests`
- Lint: `ruff check .`
- Pre-commit: `pre-commit run --all-files`

## Estrutura

| Módulo | Responsabilidade |
|--------|------------------|
| `curler/url.py` | Normalização e validação de URL (`UrlError`) |
| `curler/fetcher.py` | Subprocess `curl`, charset, split headers/body (`FetchError`) |
| `curler/parser.py` | HTML → título, texto, links `{n, text, href}` |
| `curler/renderer.py` | Saída parseada no terminal |
| `curler/style.py` | Cores ANSI (`NO_COLOR`, TTY, `--no-color`) |
| `curler/history.py` | Pilhas back/forward |
| `curler/formatter.py` | Indentação HTML (`--pretty` / REPL `pretty`) |
| `curler/cli.py` | Flags CLI, modo direto |
| `curler/repl.py` | Shell interativo Paperback |

## Convenções

- I/O `curl` só em `fetcher.py`; parse em `parser.py`; render em `renderer.py`
- `FetchResult` / `ParsedPage` são frozen dataclasses
- Testes unitários com mock; integração local em `tests/test_integration.py` (curl real)
- Commits: `feat|fix|docs(escopo): descrição` em português, imperativo

## Antes de dizer "pronto"

- `python -m unittest discover -s tests` verde
- `ruff check .` verde

## Documentação

- Guia completo: `docs/curler-guide.md`
- Decisões: `docs/decisoes/`
