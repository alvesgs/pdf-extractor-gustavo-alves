# 🗂️ GUIA DE COMANDOS GIT — PDF Extractor
# Execute esses comandos na ordem para configurar o repositório corretamente.

# ===========================================================
# 1. CONFIGURAÇÃO INICIAL (só se ainda não configurou)
# ===========================================================
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# ===========================================================
# 2. CRIAR E INICIAR O REPOSITÓRIO LOCAL
# ===========================================================
cd pdf-extractor-seu-nome    # entre na pasta do projeto
git init
git add .
git commit -m "chore: estrutura inicial do projeto"

# ===========================================================
# 3. CRIAR REPOSITÓRIO NO GITHUB
# ===========================================================
# Acesse https://github.com/new e crie: pdf-extractor-seu-nome
# Depois conecte ao remoto:
git remote add origin https://github.com/SEU-USUARIO/pdf-extractor-seu-nome.git
git branch -M main
git push -u origin main

# ===========================================================
# 4. BRANCH: feature/leitura-basica  →  PR #1
# ===========================================================
git checkout -b feature/leitura-basica

# (o código de extração básica já está em src/extrator.py)
git add src/extrator.py requirements.txt
git commit -m "feat: adiciona extração básica de texto do PDF"
git push origin feature/leitura-basica

# → Abra PR no GitHub: feature/leitura-basica → main
# → Aprove e faça merge do PR #1
git checkout main
git pull origin main

# ===========================================================
# 5. BRANCH: feature/extracao-por-paginas  →  PR #2
# ===========================================================
git checkout -b feature/extracao-por-paginas

git add src/extrator.py
git commit -m "feat: adiciona suporte à extração por páginas específicas (--pages)"
git push origin feature/extracao-por-paginas

# → Abra PR no GitHub: feature/extracao-por-paginas → main
# → Aprove e faça merge do PR #2
git checkout main
git pull origin main

# ===========================================================
# 6. BRANCH: fix/tratamento-erros  →  PR #3
# ===========================================================
git checkout -b fix/tratamento-erros

git add src/extrator.py
git commit -m "fix: adiciona tratamento de erros (arquivo inexistente, PDF criptografado, sem texto, página inválida)"
git push origin fix/tratamento-erros

# → Abra PR no GitHub: fix/tratamento-erros → main
# → Aprove e faça merge do PR #3
git checkout main
git pull origin main

# ===========================================================
# 7. DOCUMENTAÇÃO E ARQUIVOS FINAIS  →  commit em main
# ===========================================================
git add README.md CHANGELOG.md docs/ .gitignore
git commit -m "docs: adiciona README, CHANGELOG, .gitignore e pasta docs"
git push origin main

# ===========================================================
# 8. BRANCH: release/v1.0.0  →  PR #4 + TAG
# ===========================================================
git checkout -b release/v1.0.0

git add .
git commit -m "release: versão v1.0.0 — PDF Extractor funcional com documentação completa"
git push origin release/v1.0.0

# → Abra PR: release/v1.0.0 → main
# → Aprove e faça merge do PR #4
git checkout main
git pull origin main

# Criar a tag de versão
git tag -a v1.0.0 -m "release: v1.0.0 — primeira versão estável do PDF Extractor"
git push origin v1.0.0

# ===========================================================
# 9. CRIAR A RELEASE NO GITHUB
# ===========================================================
# Acesse: https://github.com/SEU-USUARIO/pdf-extractor-seu-nome/releases/new
# - Tag: v1.0.0
# - Título: PDF Extractor v1.0.0
# - Descrição:
#     ## ✅ Funcionalidades implementadas
#     - Extração completa de texto de PDFs
#     - Extração por páginas específicas (--pages)
#     - Exportação para .txt em UTF-8 (--output)
#     - Tratamento de erros: arquivo inexistente, PDF criptografado, sem texto, página inválida
#
#     ## ⚠️ Limitações conhecidas
#     - PDFs escaneados (só imagem) não têm texto extraível
#     - Não suporta senha para PDFs criptografados
#     - Não suporta OCR
#
# - Anexe o .zip do código (GitHub gera automaticamente)
