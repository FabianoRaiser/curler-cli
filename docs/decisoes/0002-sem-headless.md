# 0002 — Sem headless browser no core (curl-nativo)

- Status: aceito
- Data: 2026-07-13

## Contexto

O roadmap antigo previa **Stagecraft** (Playwright) e **Blockbuster** (Selenium) para “renderizar SPAs”. Isso exige motor JavaScript / Chromium e contradiz o pitch do Curler: *No JavaScript. No headless browser. Just the document.*

SPA client-only (shell vazio + hidratação no cliente) **não pode** ser renderizada sem engine JS. Contornar com Playwright seria trocar o motor — deixar de ser um CLI backed by `curl`.

## Decisão

1. **Rejeitar** Playwright, Selenium e qualquer browser headless neste repositório.
2. Manter o I/O HTTP **somente** via `curl` em `fetcher.py` (ADR 0001).
3. Tratar SPA CSR como **fora de escopo**: aviso no renderer + documentação; sem promessa de “próxima edição com Chromium”.
4. Próxima edição = **Hardbound**: aprofundar curl (headers de request, POST, cookies, save, timeout/UA).

Issues Linear CRU-38 e CRU-39 foram canceladas sob esta decisão.

## Consequências

- (+) Identidade de produto coerente (nome Curler = curl)
- (+) Pacote leve; CI e instalação simples
- (+) Roadmap claro: sessão HTTP, não runtime JS
- (−) Sites CSR puro continuam ilegíveis além do shell — e isso é aceito de propósito
- (−) Quem precisar de browser headless deve usar outra ferramenta

## Alternativas consideradas

| Alternativa | Por que não |
|---|---|
| Flag `--engine=browser` opcional | Ainda puxa Chromium para o ecossistema Curler e confunde o core |
| Repo irmão `curler-stagecraft` | Possível no futuro, mas **não** é edição deste projeto |
| Heurísticas / chamar APIs JSON da SPA | Útil como feature pontual; não é “renderizar SPA” |

## Referências

- ADR 0001 — curl via subprocess
- `docs/curler-guide.md` — tabela de edições e roadmap
- Linear: CRU-38, CRU-39 (canceladas), milestone Hardbound v0.3
