# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adota o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [v1.0.0] - 2026-02-19

### Added
- Extração completa de texto de arquivos PDF usando `pypdf`
- Suporte à extração de páginas específicas via argumento `--pages`
  - Aceita página única: `--pages 1`
  - Aceita intervalos: `--pages 1-3`
  - Aceita combinações: `--pages 1-3,5,10`
- Exportação do texto extraído para arquivo `.txt` em UTF-8 via `--output`
- Exibição do texto no terminal quando `--output` não é informado
- Tratamento de erros para:
  - Arquivo PDF inexistente
  - PDF criptografado/protegido por senha
  - PDF sem texto extraível (apenas imagens)
  - Página fora do intervalo do documento
  - Formato de páginas inválido
- Código organizado em funções modulares com docstrings
- Interface de linha de comando (CLI) com `argparse`
- Mensagens de feedback visuais com emojis no terminal
- Estrutura de projeto com `/src`, `/docs`, `README.md`, `CHANGELOG.md`, `requirements.txt`

### Changed
- N/A (primeira versão)

### Fixed
- N/A (primeira versão)

---

## [Não lançado]

- Suporte a PDFs escaneados via OCR (ex: `pytesseract`)
- Modo interativo para seleção de arquivo via menu
- Exportação para outros formatos (`.csv`, `.json`)
- Suporte a senha para PDFs criptografados

---

## Histórico de branches e PRs

| Branch                          | PR  | Descrição                              | Status   |
|---------------------------------|-----|----------------------------------------|----------|
| `feature/leitura-basica`        | #1  | Leitura e extração básica de texto     | ✅ merged |
| `feature/extracao-por-paginas`  | #2  | Extração por páginas específicas       | ✅ merged |
| `fix/tratamento-erros`          | #3  | Tratamento de erros e validações       | ✅ merged |
| `release/v1.0.0`                | #4  | Versão final com documentação completa | ✅ merged |
