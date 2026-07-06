# Changelog

## [Unreleased]

### Added
- Paperback edition: parsed page output by default, `--raw` for HTML source
- REPL navigation: `links`, `go <n>`, `back`, `forward`

### Changed
- Links inline `[n]` no texto; lista completa só via comando `links`; contador no rodapé

### Fixed
- Decodificação correta de páginas em ISO-8859-1 e outros charsets declarados

## [0.1.0] - 2026-07-03

### Added
- Manuscript CLI browser (fetch, REPL, `--pretty`)
- CI, pre-commit, release workflow