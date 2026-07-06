---
name: comando-repl
description: >
  Passo a passo para adicionar um novo comando ao REPL interativo do Curler
  Manuscript. Use quando o pedido for criar comando tipo headers, raw, pretty.
---

# Novo comando REPL

Siga exatamente esta ordem:

1. Adicione o comando em `curler/repl.py` no loop de `run_repl()`.
2. Atualize `HELP_TEXT` com descrição curta.
3. Comandos que usam `last_response` devem tratar `None` com mensagem em stderr.
4. Comandos que navegam devem usar `normalize_url` + `fetch_func` (já injetável).
5. Escreva testes em `tests/test_repl.py` com `input_func` mockado.
6. Atualize `README.md` na seção do REPL.
7. Rode `python -m unittest discover -s tests` e `ruff check .`. Só então finalize.

Mantenha `fetch_func` e `input_func` injetáveis para testes sem rede.
