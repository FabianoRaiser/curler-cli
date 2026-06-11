# Curler — The Web, Unmasked

> *"Because the web had words before it had JavaScript."*

O Curler é um navegador CLI construído em cima do `curl`. Sem GPU, sem engine JavaScript, sem 300MB de Chromium — só uma conexão TCP, um parser de HTML e a audácia de chamar isso de navegador. A web moderna empilhou camadas de teatro sobre o que é, no fundo, um sistema de entrega de documentos. O Curler arranca esse teatro e te mostra o roteiro.

O projeto vem em quatro edições que seguem essa metáfora sem vergonha. O **Manuscript** te entrega o HTML cru exatamente como o servidor escreveu — sem interpretação, sem piedade. O **Paperback** parseia essa marcação e te devolve algo legível: título, texto, links. O **Stagecraft** sobe um browser headless, monta o palco sem plateia e deixa o JavaScript rodar o suficiente pra popular a página. O **Blockbuster** vai de Selenium completo — o cinema inteiro, alugado, pra um único request. Cada edição é uma troca deliberada entre peso e compatibilidade, e uma aula sobre quanta infraestrutura a web moderna silenciosamente exige de você.

---

## Edições

| Edição | Tecnologia | Peso | Funciona em SPAs? |
|---|---|---|---|
| **Manuscript** | curl puro | ~200KB | Não — HTML cru |
| **Paperback** | curl + BeautifulSoup | ~15MB | Não — avisa o usuário |
| **Stagecraft** | curl + Playwright headless | ~300MB | Parcialmente |
| **Blockbuster** | curl + Selenium + Chrome | ~500MB+ | Sim |

---

## Arquitetura (Paperback)

```
[ Input do usuário ]
        │
        ▼
[ URL Parser ]          → normaliza, adiciona https://, valida
        │
        ▼
[ curl subprocess ]     → faz o request, captura headers + body
        │
        ▼
[ Response Inspector ]  → lê status code, content-type, redirects
        │
      ┌─┴──────────────────────┐
      ▼                        ▼
[ HTML Parser ]          [ Raw mode ]
  BeautifulSoup            exibe como texto
      │
      ▼
[ Renderer ]             → título, texto limpo, links numerados
        │
        ▼
[ History Manager ]      → pilha back / stack forward
        │
        ▼
[ REPL ]                 → loop interativo aguarda próximo comando
```

---

## Comandos do REPL

| Comando | O que faz |
|---|---|
| `<url>` | Navega para a URL |
| `back` | Volta no histórico |
| `forward` | Avança no histórico |
| `links` | Lista todos os links da página atual |
| `go <n>` | Segue o link de número N |
| `raw` | Mostra o HTML bruto da página atual |
| `headers` | Mostra os response headers |
| `help` | Lista os comandos disponíveis |
| `quit` | Encerra o Curler |

---

## Pré-requisitos

- Python 3.10+
- curl instalado no sistema (`which curl`)
- pip

---

## Instalação (Paperback)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/curler.git
cd curler

# Instale as dependências Python
pip install beautifulsoup4 lxml

# Torne o script executável
chmod +x curler.py

# Execute
python curler.py
```

---

## Estrutura de arquivos sugerida

```
curler/
├── curler.py          # Entry point — REPL principal
├── fetcher.py         # Wrapper do curl (subprocess)
├── parser.py          # HTML → estrutura legível (BeautifulSoup)
├── renderer.py        # Formata e imprime no terminal
├── history.py         # Gerencia pilha de navegação
└── README.md
```

---

## Decisões de design

### Sites que vão quebrar
O Curler funciona bem em sites com **server-side rendering**: Wikipedia, blogs, portais de notícia, documentação, GitHub. Em SPAs (React, Angular, Vue), o HTML retornado costuma ser um `<div id="root"></div>` vazio — o Curler detecta isso e avisa o usuário.

### Por que não Selenium ou Playwright no Paperback?
- Selenium: 4 processos se comunicando em rede só pra ler texto. É alugar um ônibus pra ir sozinho na padaria.
- Playwright headless: ~300MB de Chromium pra servir como estenógrafo de um palco que ninguém vai ver.
- O Curler Paperback é uma lambreta. A leveza é uma feature, não uma limitação.

### Redirects
O curl segue redirects automaticamente com a flag `-L`. O Curler registra cada URL visitada no histórico, incluindo a URL final após redirecionamentos.

---

## Roadmap

- [x] **Manuscript** — curl puro, output HTML bruto
- [ ] **Paperback** — parser + abstração legível + REPL + histórico
- [ ] Suporte a `POST` com body customizado
- [ ] Headers customizados (`-H`)
- [ ] Salvar resposta em arquivo (`save <filename>`)
- [ ] **Stagecraft** — integração com Playwright headless
- [ ] **Blockbuster** — integração com Selenium
