# 0001 — curl via subprocess, sem dependências Python

- Status: aceito
- Data: 2026-07-06

## Contexto

A edição Manuscript do Curler deve ser leve (~200KB), executável com Python stdlib e o `curl` já instalado no sistema. O objetivo é entregar HTML cru sem interpretação.

## Decisão

Usar `subprocess` para invocar o `curl` do sistema. Funções de domínio expostas e testáveis:

- `build_curl_command()` — monta args sem executar
- `split_headers_and_body()` — separa headers finais do body após redirects
- `fetch()` — orquestra subprocess e retorna `FetchResult`

Testes usam `unittest.mock` em `subprocess.run` — nunca requisições de rede reais.

## Consequências

- (+) Zero dependências Python na edição Manuscript
- (+) Reutiliza `curl` maduro (redirects com `-L`, headers com `-D`)
- (+) Funções puras triviais de testar com mock
- (−) Depende de `curl` no `PATH`
- (−) Sem controle fino de timeout/retry até implementar flags explícitas

## Evolução

Se a edição **Paperback** entrar, criar ADR 0002 para BeautifulSoup em módulo separado (`parser.py`), sem alterar `fetcher.py`. Stagecraft/Blockbuster terão ADRs próprios para Playwright/Selenium.
