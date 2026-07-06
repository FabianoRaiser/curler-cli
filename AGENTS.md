# Curler Manuscript

CLI que busca URLs via `curl` do sistema e imprime HTML cru. Edição **Manuscript**: sem JavaScript, sem parser de conteúdo, sem dependências Python externas.

## Stack

- Python 3.10+, stdlib only (Manuscript)
- `curl` instalado e disponível no `PATH`
- `unittest` (stdlib), `ruff` (dev)

## Comandos

- Instalar: `pip install -e .`
- Testes: `python -m unittest discover -s tests`
- Lint: `ruff check .`
- Formatar: `ruff format .`
- Pre-commit: `pre-commit run --all-files`

## Estrutura

| Módulo | Responsabilidade |
|--------|------------------|
| `curler/url.py` | Normalização e validação de URL (`UrlError`) |
| `curler/fetcher.py` | Subprocess `curl`, split headers/body (`FetchError`) |
| `curler/formatter.py` | Indentação legível de HTML (sem interpretar conteúdo) |
| `curler/cli.py` | Argumentos, flags, modo direto |
| `curler/repl.py` | Shell interativo Manuscript |

## Convenções

- I/O (subprocess `curl`) só em `fetcher.py`; CLI/REPL em `cli.py` / `repl.py`
- `FetchResult` é `frozen` dataclass
- Erros de URL → `UrlError`; erros de rede/curl → `FetchError`
- Testes usam `unittest.mock` — nunca batem na rede real
- Commits: `feat|fix|chore(escopo): descrição` em português, imperativo

## Regras de domínio (inegociáveis)

- Só `http://` e `https://`; host obrigatório
- `curl` deve existir no `PATH` antes de `fetch`
- Manuscript **não** parseia HTML em texto legível (isso é Paperback — ver `docs/curler-guide.md`)
- Flags mutuamente exclusivas devem ser validadas em `build_parser` / `main`

## Antes de dizer "pronto"

- `python -m unittest discover -s tests` verde
- `ruff check .` verde

## Documentação

- Roadmap e arquitetura Paperback: `docs/curler-guide.md`
- Decisões arquiteturais: `docs/decisoes/`
