# Curler — The Web, Unmasked

> *"Because the web had words before it had JavaScript."*

O Curler é um navegador CLI construído em cima do `curl`. Sem GPU, sem engine JavaScript, sem 300MB de Chromium — só uma conexão TCP, um parser de HTML e a audácia de chamar isso de navegador.

O projeto vem em edições **sempre em cima do curl do sistema** — sem Playwright, sem Selenium, sem Chromium. O **Manuscript** entrega HTML cru. O **Paperback** (v0.2 — **atual**) parseia a marcação em páginas legíveis com navegação no REPL. O **Hardbound** (próxima) aprofunda a sessão HTTP via flags do curl.

---

## Edições

| Edição | Tecnologia | Peso | SPAs client-only? |
|---|---|---|---|
| **Manuscript** | curl puro | ~200KB | Não — HTML cru |
| **Paperback** | curl + BeautifulSoup | ~15MB | Não — avisa o usuário |
| **Hardbound** | curl (headers, POST, cookies, save, …) | ~15MB | Não — fora de escopo |

Filosofia: o Curler lê o **documento HTTP** que o servidor envia. Renderizar SPA client-side exige motor JS e desvirtua o produto — ver [ADR 0002](decisoes/0002-sem-headless.md).

---

## Arquitetura (Paperback v0.2)

```
[ Input do usuário ]
        │
        ▼
[ url.py ]              → normaliza, adiciona https://, valida
        │
        ▼
[ fetcher.py ]          → curl -L, charset, headers + body
        │
      ┌─┴──────────────────────┐
      ▼                        ▼
[ parser.py ]            [ --raw / --pretty ]
  BeautifulSoup            formatter.py (HTML indentado)
      │
      ▼
[ renderer.py + style.py ] → título, texto, refs [n], cores ANSI
        │
        ▼
[ history.py ]          → pilha back / forward (REPL)
        │
        ▼
[ repl.py / cli.py ]
```

---

## Saída parseada (default)

Exemplo de página renderizada:

```text
Example Site

# Getting Started

Read the Docs [1] or visit our Blog [2].

- Item one
- Item two

1. First step
2. Second step

(2 links — use links)
```

- **Título** da tag `<title>` no topo
- **Headings** com `#`, `##`, … conforme h1–h6
- **Links inline** `[n]` ao lado do texto âncora
- **Listas** com `-` (ul) e `1.` (ol)
- **Rodapé** com contagem de links; no REPL inclui dica `use links`
- **Cores ANSI** em terminal (links azuis, headings destacados); desligadas com `--no-color`, `NO_COLOR` ou pipe
- **`links`** no REPL lista URLs completas

Modo Manuscript: `curler --raw URL` ou `pretty` no REPL.

---

## Flags CLI

| Flag | Efeito |
|---|---|
| *(default)* | Saída parseada |
| `--raw` | HTML bruto |
| `--pretty` | HTML indentado |
| `--no-color` | Sem cores ANSI |
| `--headers` | Só response headers |
| `--include-headers` | Headers + body |

---

## Comandos do REPL

| Comando | O que faz |
|---|---|
| `<url>` | Navega para a URL |
| `links` | Lista links numerados com URLs |
| `go <n>` | Segue o link N |
| `back` | Volta no histórico |
| `forward` | Avança no histórico |
| `raw` | HTML bruto da página atual |
| `pretty` | HTML indentado da página atual |
| `headers` | Response headers |
| `help` | Ajuda |
| `quit` / `exit` | Sair |

---

## Instalação

```bash
git clone https://github.com/FabianoRaiser/curler-cli.git
cd curler-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
curler --version   # curler 0.2.2
```

---

## Estrutura do repositório

```
curler/
├── cli.py           # Entry point CLI
├── fetcher.py       # curl subprocess + charset
├── parser.py        # HTML → ParsedPage
├── renderer.py      # format_body, render_page
├── style.py         # ANSI Stylizer
├── history.py       # back/forward
├── formatter.py     # --pretty (Manuscript)
├── repl.py          # REPL interativo
└── url.py           # normalize_url
tests/
├── fixtures/        # HTML de exemplo
├── test_parser.py
├── test_integration.py  # HTTP local + curl real
└── ...
```

---

## Decisões de design

### Sites que funcionam bem
Wikipedia, blogs, documentação, portais com **server-side rendering**.

### SPAs e Framer
SPAs client-only (React/Vue com shell vazio) costumam retornar `<div id="root"></div>` — o Curler avisa e **não** tenta executar JavaScript. Sites com SSR/HTML no primeiro response funcionam bem. Sites **Framer** podem ter HTML verboso e texto duplicado; comentários SSR (`<!--$-->`) são ignorados desde v0.2.

### Redirects
O curl segue redirects com `-L`. O histórico REPL guarda cada página visitada com body cacheado.

### Charset
O fetcher detecta charset em `Content-Type` e `<meta charset>`, com fallback UTF-8 → Latin-1.

---

## Roadmap

- [x] **Manuscript** v0.1 — curl puro, HTML bruto
- [x] **Paperback** v0.2 — parser, renderer, REPL, histórico, cores
- [ ] **Hardbound** v0.3 — sessão curl:
  - [x] Headers de request (`-H`)
  - [ ] POST / body (`-X` / `--data`)
  - [x] Cookies / cookie-jar (`-b` / `-c`)
  - [ ] Timeout e User-Agent
  - [ ] Salvar resposta (`save` / `--output`)
- [x] ~~Stagecraft / Blockbuster (headless)~~ — **rejeitados** ([ADR 0002](decisoes/0002-sem-headless.md))
