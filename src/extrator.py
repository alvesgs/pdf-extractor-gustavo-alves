"""
PDF Extractor - Ferramenta de extração de texto de PDFs
DocuMaster Solutions

Uso:
    python extrator.py --input arquivo.pdf
    python extrator.py --input arquivo.pdf --pages 1
    python extrator.py --input arquivo.pdf --pages 1-3,5,10
    python extrator.py --input arquivo.pdf --output resultado.txt
"""

import argparse
import sys
import os
from pypdf import PdfReader
from pypdf.errors import PdfReadError


def parse_page_ranges(pages_str: str, total_pages: int) -> list[int]:
    """
    Converte uma string de intervalos de páginas em uma lista de índices (0-based).

    Args:
        pages_str: String no formato "1,3-5,7" (números baseados em 1)
        total_pages: Número total de páginas do PDF

    Returns:
        Lista de índices de página (0-based), sem duplicatas, ordenada.

    Raises:
        ValueError: Se o formato for inválido ou página fora do intervalo.
    """
    indices = set()
    parts = pages_str.split(",")

    for part in parts:
        part = part.strip()
        if "-" in part:
            bounds = part.split("-")
            if len(bounds) != 2:
                raise ValueError(f"Intervalo inválido: '{part}'")
            start, end = int(bounds[0]), int(bounds[1])
            if start < 1 or end < start:
                raise ValueError(f"Intervalo inválido: '{part}'")
            if end > total_pages:
                raise ValueError(
                    f"Página {end} fora do intervalo. O PDF tem {total_pages} página(s)."
                )
            for p in range(start, end + 1):
                indices.add(p - 1)  # converte para 0-based
        else:
            page_num = int(part)
            if page_num < 1 or page_num > total_pages:
                raise ValueError(
                    f"Página {page_num} fora do intervalo. O PDF tem {total_pages} página(s)."
                )
            indices.add(page_num - 1)

    return sorted(indices)


def open_pdf(filepath: str) -> PdfReader:
    """
    Abre e valida um arquivo PDF.

    Args:
        filepath: Caminho para o arquivo PDF.

    Returns:
        Objeto PdfReader pronto para leitura.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o arquivo for criptografado ou inválido.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: '{filepath}'")

    try:
        reader = PdfReader(filepath)
    except PdfReadError as e:
        raise ValueError(f"Erro ao ler o PDF: {e}")

    if reader.is_encrypted:
        raise ValueError(
            "Este PDF está criptografado. Forneça a senha ou use um PDF sem proteção."
        )

    return reader


def extract_text_from_pages(reader: PdfReader, page_indices: list[int]) -> str:
    """
    Extrai texto das páginas especificadas.

    Args:
        reader: Objeto PdfReader já aberto.
        page_indices: Lista de índices de página (0-based).

    Returns:
        Texto extraído concatenado de todas as páginas.

    Raises:
        ValueError: Se nenhum texto extraível for encontrado.
    """
    texts = []

    for idx in page_indices:
        page = reader.pages[idx]
        text = page.extract_text() or ""
        header = f"\n{'='*60}\n📄 PÁGINA {idx + 1}\n{'='*60}\n"
        texts.append(header + text)

    full_text = "\n".join(texts).strip()

    if not full_text.replace("=", "").replace("📄", "").replace("PÁGINA", "").strip():
        raise ValueError(
            "Nenhum texto extraível encontrado. "
            "O PDF pode conter apenas imagens ou texto escaneado."
        )

    return full_text


def save_output(text: str, output_path: str) -> None:
    """
    Salva o texto extraído em um arquivo .txt em UTF-8.

    Args:
        text: Texto a ser salvo.
        output_path: Caminho do arquivo de saída.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Texto salvo em: {output_path}")


def build_arg_parser() -> argparse.ArgumentParser:
    """Configura e retorna o parser de argumentos da CLI."""
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
    parser.add_argument("--input", required=True, help="Caminho para o arquivo PDF de entrada")
    parser.add_argument(
        "--pages",
        default=None,
        help='Páginas a extrair. Ex: "1", "1-3", "1-3,5,10". Padrão: todas.',
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Caminho para salvar o texto extraído (.txt). Se omitido, exibe no terminal.",
    )
    return parser


def main():
    """Ponto de entrada principal da aplicação."""
    parser = build_arg_parser()
    args = parser.parse_args()

    print("🔍 PDF Extractor - DocuMaster Solutions")
    print("-" * 40)

    # 1. Abrir o PDF
    try:
        reader = open_pdf(args.input)
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)

    total_pages = len(reader.pages)
    print(f"📂 Arquivo: {args.input}")
    print(f"📑 Total de páginas: {total_pages}")

    # 2. Determinar páginas a extrair
    if args.pages:
        try:
            page_indices = parse_page_ranges(args.pages, total_pages)
        except ValueError as e:
            print(f"❌ Erro nas páginas informadas: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"📌 Páginas selecionadas: {[i + 1 for i in page_indices]}")
    else:
        page_indices = list(range(total_pages))
        print("📌 Extraindo todas as páginas...")

    # 3. Extrair texto
    try:
        text = extract_text_from_pages(reader, page_indices)
    except ValueError as e:
        print(f"❌ Erro na extração: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Exibir ou salvar
    if args.output:
        save_output(text, args.output)
    else:
        print("\n" + "=" * 60)
        print("📝 TEXTO EXTRAÍDO")
        print("=" * 60)
        print(text)

    print("\n✅ Extração concluída com sucesso!")


if __name__ == "__main__":
    main()
