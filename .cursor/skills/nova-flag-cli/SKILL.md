---
name: nova-flag-cli
description: >
  Passo a passo para adicionar uma nova flag ao CLI do Curler Manuscript
  (ex.: --timeout, --user-agent). Use quando o pedido for criar ou alterar
  flags de linha de comando.
---

# Nova flag CLI

Siga exatamente esta ordem:

1. Adicione o argumento em `curler/cli.py` (`build_parser`).
2. Valide combinações incompatíveis em `main()` antes do fetch (padrão: `--headers` + `--pretty`).
3. Se a flag altera o comando curl, atualize `build_curl_command()` em `curler/fetcher.py`.
4. Escreva testes em `tests/test_cli.py`: caminho feliz + pelo menos uma combinação inválida.
5. Se `fetcher` mudou, adicione testes em `tests/test_fetcher.py` com mock de subprocess.
6. Atualize `README.md` com exemplo de uso.
7. Rode `python -m unittest discover -s tests` e `ruff check .`. Só então finalize.

Não adicione dependências externas na edição Manuscript.
