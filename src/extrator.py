# -*- coding: utf-8 -*-
"""
PDF Extractor - Ferramenta de extração de texto de PDFs
DocuMaster Solutions

Modo interativo: basta rodar o script e seguir as instruções.
Modo CLI:
    python extrator.py --input arquivo.pdf
    python extrator.py --input arquivo.pdf --pages 1-3,5
    python extrator.py --input arquivo.pdf --output resultado.txt
"""

import argparse
import sys
import os
from pypdf import PdfReader
from pypdf.errors import PdfReadError


# ──────────────────────────────────────────────
# FUNÇÕES PRINCIPAIS
# ──────────────────────────────────────────────

def parse_page_ranges(pages_str: str, total_pages: int) -> list:
    """
    Converte uma string de intervalos de páginas em lista de índices (0-based).

    Args:
        pages_str: Ex: "1", "1-3", "1-3,5,10"
        total_pages: Total de páginas do PDF

    Returns:
        Lista ordenada de índices (0-based)

    Raises:
        ValueError: Formato inválido ou página fora do intervalo
    """
    indices = set()
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            bounds = part.split("-")
            if len(bounds) != 2:
                raise ValueError(f"Intervalo inválido: '{part}'")
            start, end = int(bounds[0]), int(bounds[1])
            if start < 1 or end < start:
                raise ValueError(f"Intervalo inválido: '{part}'")
            if end > total_pages:
                raise ValueError(f"Página {end} fora do intervalo. O PDF tem {total_pages} página(s).")
            for p in range(start, end + 1):
                indices.add(p - 1)
        else:
            page_num = int(part)
            if page_num < 1 or page_num > total_pages:
                raise ValueError(f"Página {page_num} fora do intervalo. O PDF tem {total_pages} página(s).")
            indices.add(page_num - 1)
    return sorted(indices)


def open_pdf(filepath: str) -> PdfReader:
    """
    Abre e valida um arquivo PDF.

    Raises:
        FileNotFoundError: Arquivo não encontrado
        ValueError: PDF criptografado ou inválido
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: '{filepath}'")
    try:
        reader = PdfReader(filepath)
    except PdfReadError as e:
        raise ValueError(f"Erro ao ler o PDF: {e}")
    if reader.is_encrypted:
        raise ValueError("Este PDF está criptografado. Use um PDF sem proteção por senha.")
    return reader


def extract_text_from_pages(reader: PdfReader, page_indices: list) -> str:
    """
    Extrai texto das páginas indicadas.

    Raises:
        ValueError: Nenhum texto extraível encontrado
    """
    texts = []
    for idx in page_indices:
        page = reader.pages[idx]
        text = page.extract_text() or ""
        header = f"\n{'='*60}\n  PAGINA {idx + 1}\n{'='*60}\n"
        texts.append(header + text)

    full_text = "\n".join(texts).strip()

    sem_cabecalho = full_text.replace("=", "").replace("PAGINA", "").strip()
    if not sem_cabecalho:
        raise ValueError("Nenhum texto extraível encontrado. O PDF pode conter apenas imagens.")

    return full_text


def save_output(text: str, output_path: str) -> None:
    """Salva o texto extraído em arquivo .txt (UTF-8)."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\n  Texto salvo com sucesso em: {output_path}")


# ──────────────────────────────────────────────
# MODO INTERATIVO
# ──────────────────────────────────────────────

def modo_interativo():
    """Guia o usuário passo a passo pelo processo de extração."""

    print()
    print("=" * 55)
    print("   PDF EXTRACTOR - DocuMaster Solutions")
    print("   Extrator de texto de arquivos PDF")
    print("=" * 55)
    print()

    # ── PASSO 1: caminho do arquivo ──
    print("[ PASSO 1 ] Informe o caminho do arquivo PDF")
    print("  Dica: arraste o arquivo para o terminal ou cole o caminho completo")
    print()

    while True:
        filepath = input("  Caminho do PDF: ").strip().strip('"').strip("'")
        if not filepath:
            print("  ERRO: Nenhum caminho informado. Tente novamente.\n")
            continue
        try:
            reader = open_pdf(filepath)
            break
        except (FileNotFoundError, ValueError) as e:
            print(f"  ERRO: {e}\n")

    total_pages = len(reader.pages)
    print(f"\n  Arquivo carregado com sucesso!")
    print(f"  Total de paginas encontradas: {total_pages}\n")

    # ── PASSO 2: quais páginas ──
    print("─" * 55)
    print("[ PASSO 2 ] Quais paginas deseja extrair?")
    print()
    print("  [1] Todas as paginas")
    print("  [2] Escolher paginas especificas")
    print()

    while True:
        opcao_paginas = input("  Sua escolha (1 ou 2): ").strip()
        if opcao_paginas in ("1", "2"):
            break
        print("  ERRO: Digite 1 ou 2.\n")

    if opcao_paginas == "1":
        page_indices = list(range(total_pages))
        print(f"\n  Todas as {total_pages} paginas serao extraidas.")
    else:
        print()
        print(f"  O PDF tem {total_pages} pagina(s).")
        print("  Exemplos validos: 1 | 1-3 | 1-3,5,10")
        print()
        while True:
            paginas_input = input("  Paginas desejadas: ").strip()
            try:
                page_indices = parse_page_ranges(paginas_input, total_pages)
                print(f"\n  Paginas selecionadas: {[i+1 for i in page_indices]}")
                break
            except ValueError as e:
                print(f"  ERRO: {e}\n")

    # ── PASSO 3: extrair ──
    print()
    print("─" * 55)
    print("[ PASSO 3 ] Extraindo texto...")
    print()

    try:
        text = extract_text_from_pages(reader, page_indices)
    except ValueError as e:
        print(f"  ERRO: {e}")
        sys.exit(1)

    print("  Texto extraido com sucesso!")

    # ── PASSO 4: salvar ou exibir ──
    print()
    print("─" * 55)
    print("[ PASSO 4 ] O que deseja fazer com o texto extraido?")
    print()
    print("  [1] Exibir no terminal")
    print("  [2] Salvar em arquivo .txt")
    print("  [3] Fazer os dois")
    print()

    while True:
        opcao_saida = input("  Sua escolha (1, 2 ou 3): ").strip()
        if opcao_saida in ("1", "2", "3"):
            break
        print("  ERRO: Digite 1, 2 ou 3.\n")

    if opcao_saida in ("1", "3"):
        print()
        print("=" * 55)
        print("  TEXTO EXTRAIDO")
        print("=" * 55)
        print(text)

    if opcao_saida in ("2", "3"):
        print()
        nome_sugerido = os.path.splitext(os.path.basename(filepath))[0] + "_extraido.txt"
        print(f"  Nome sugerido: {nome_sugerido}")
        nome_arquivo = input("  Nome do arquivo .txt (Enter para usar o sugerido): ").strip()
        if not nome_arquivo:
            nome_arquivo = nome_sugerido
        if not nome_arquivo.endswith(".txt"):
            nome_arquivo += ".txt"
        save_output(text, nome_arquivo)

    print()
    print("=" * 55)
    print("  EXTRACAO CONCLUIDA COM SUCESSO!")
    print("=" * 55)
    print()
    input("  Pressione Enter para sair...")


# ──────────────────────────────────────────────
# MODO CLI (linha de comando)
# ──────────────────────────────────────────────

def build_arg_parser() -> argparse.ArgumentParser:
    """Configura o parser de argumentos da CLI."""
    parser = argparse.ArgumentParser(
        description="PDF Extractor - Extrai texto de arquivos PDF",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Exemplos:\n"
            "  python extrator.py --input doc.pdf\n"
            "  python extrator.py --input doc.pdf --pages 1\n"
            "  python extrator.py --input doc.pdf --pages 1-3,5,10\n"
            "  python extrator.py --input doc.pdf --output resultado.txt\n"
        ),
    )
    parser.add_argument("--input", help="Caminho para o arquivo PDF de entrada")
    parser.add_argument("--pages", default=None, help='Paginas a extrair. Ex: "1", "1-3", "1-3,5,10"')
    parser.add_argument("--output", default=None, help="Arquivo .txt de saida (opcional)")
    return parser


def modo_cli(args):
    """Executa a extração via argumentos de linha de comando."""
    print("\n  PDF Extractor - DocuMaster Solutions")
    print("-" * 40)

    try:
        reader = open_pdf(args.input)
    except (FileNotFoundError, ValueError) as e:
        print(f"  ERRO: {e}", file=sys.stderr)
        sys.exit(1)

    total_pages = len(reader.pages)
    print(f"  Arquivo: {args.input}")
    print(f"  Total de paginas: {total_pages}")

    if args.pages:
        try:
            page_indices = parse_page_ranges(args.pages, total_pages)
        except ValueError as e:
            print(f"  ERRO: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"  Paginas selecionadas: {[i + 1 for i in page_indices]}")
    else:
        page_indices = list(range(total_pages))
        print("  Extraindo todas as paginas...")

    try:
        text = extract_text_from_pages(reader, page_indices)
    except ValueError as e:
        print(f"  ERRO: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        save_output(text, args.output)
    else:
        print("\n" + "=" * 60)
        print("  TEXTO EXTRAIDO")
        print("=" * 60)
        print(text)

    print("\n  Extracao concluida com sucesso!\n")


# ──────────────────────────────────────────────
# PONTO DE ENTRADA
# ──────────────────────────────────────────────

def main():
    """
    Decide automaticamente entre modo interativo e modo CLI.
    - Sem argumentos → modo interativo (menu passo a passo)
    - Com --input    → modo CLI direto
    """
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.input:
        modo_cli(args)
    else:
        modo_interativo()


if __name__ == "__main__":
    main()
