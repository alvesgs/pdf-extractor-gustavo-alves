# 📄 PDF Extractor

> Ferramenta de extração de texto de arquivos PDF desenvolvida em Python.  
> Projeto avaliativo – DocuMaster Solutions | UC9

---

## 📋 Descrição

O **PDF Extractor** é uma ferramenta de linha de comando (CLI) desenvolvida em Python que permite extrair texto de arquivos PDF de forma simples e rápida. Suporta extração de páginas específicas, tratamento de erros comuns e exportação do resultado para arquivo `.txt`.

---

## ⚙️ Requisitos do Sistema

- Python **3.10** ou superior
- pip (gerenciador de pacotes Python)
- Sistema operacional: Windows, Linux ou macOS

---

## 🚀 Como Instalar

**1. Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/pdf-extractor-seu-nome.git
cd pdf-extractor-seu-nome
```

**2. (Opcional, mas recomendado) Crie um ambiente virtual:**

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

---

## ▶️ Como Executar

O script principal está em `src/extrator.py`.

### Extrair todo o texto de um PDF (exibe no terminal)

```bash
python src/extrator.py --input documento.pdf
```

### Extrair e salvar em arquivo `.txt`

```bash
python src/extrator.py --input documento.pdf --output resultado.txt
```

### Extrair apenas a página 1

```bash
python src/extrator.py --input documento.pdf --pages 1
```

### Extrair um intervalo de páginas (1 a 3)

```bash
python src/extrator.py --input documento.pdf --pages 1-3
```

### Extrair páginas específicas e não sequenciais

```bash
python src/extrator.py --input documento.pdf --pages 1-3,5,10
```

### Ver ajuda completa

```bash
python src/extrator.py --help
```

---

## 🧩 Argumentos disponíveis

| Argumento  | Obrigatório | Descrição                                                   |
|------------|-------------|-------------------------------------------------------------|
| `--input`  | ✅ Sim       | Caminho para o arquivo PDF de entrada                       |
| `--pages`  | ❌ Não       | Páginas a extrair (ex: `1`, `1-3`, `1-3,5,10`). Padrão: todas |
| `--output` | ❌ Não       | Caminho do arquivo `.txt` de saída. Se omitido, exibe no terminal |

---

## 🛡️ Tratamento de Erros

A ferramenta trata os seguintes erros automaticamente:

| Situação                          | Mensagem exibida                                              |
|-----------------------------------|---------------------------------------------------------------|
| Arquivo não encontrado            | `❌ Erro: Arquivo não encontrado: 'arquivo.pdf'`              |
| PDF criptografado                 | `❌ Erro: Este PDF está criptografado...`                     |
| PDF sem texto extraível           | `❌ Erro: Nenhum texto extraível encontrado...`               |
| Página fora do intervalo          | `❌ Erro: Página X fora do intervalo. O PDF tem Y página(s).` |
| Formato de páginas inválido       | `❌ Erro nas páginas informadas: Intervalo inválido: '...'`   |

---

## 📁 Estrutura do Projeto

```
pdf-extractor-seu-nome/
│
├── src/
│   └── extrator.py        # Script principal da aplicação
│
├── docs/
│   └── prints/            # Prints da execução da aplicação
│
├── README.md              # Documentação do projeto
├── CHANGELOG.md           # Histórico de versões
└── requirements.txt       # Dependências do projeto
```

---

## 🌿 Branches utilizadas

| Branch                        | Finalidade                                      |
|-------------------------------|-------------------------------------------------|
| `main`                        | Branch principal com código estável             |
| `feature/leitura-basica`      | Leitura e extração básica de texto do PDF       |
| `feature/extracao-por-paginas`| Suporte à extração de páginas específicas       |
| `fix/tratamento-erros`        | Tratamento de erros e validações                |
| `release/v1.0.0`              | Versão final do projeto                         |

---

## 📦 Versão atual

**v1.0.0** — Primeira versão estável.  
Consulte o [CHANGELOG.md](CHANGELOG.md) para o histórico completo.

---

## 👤 Autor

Desenvolvido como atividade avaliativa final da UC9.  
**DocuMaster Solutions** — Automação de documentos digitais.
