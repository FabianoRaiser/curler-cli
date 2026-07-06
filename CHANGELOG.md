# Changelog

## [0.2.2] - 2026-07-06

### Fixed

- Workflow de release: remove commit/push do CHANGELOG em detached HEAD; git-cliff gera só as release notes

## [0.2.1] - 2026-07-06

### Fixed

- Workflow de release: git-cliff exige `--latest` ou `--unreleased` para definir o intervalo de commits

## [0.2.0] - 2026-07-06

### Added

- Paperback edition: parsed page output by default, `--raw` for HTML source
- Parser HTML (BeautifulSoup + lxml), renderer e histórico back/forward
- REPL navigation: `links`, `go <n>`, `back`, `forward`
- Links inline `[n]` no texto; lista completa via comando `links`
- Headings h1–h6 com marcadores `#`/`##`/…; listas com `-` e numeração `1.`
- Saída parseada com cores ANSI; `--no-color` e `NO_COLOR`

### Fixed

- Decodificação correta de páginas em ISO-8859-1 e outros charsets declarados
- Comentários HTML (ex.: marcadores SSR do Framer) não aparecem mais como `$` na saída

## [0.1.0] - 2026-07-03

### Added

- Manuscript CLI browser (fetch, REPL, `--pretty`)
- CI, pre-commit, release workflow
