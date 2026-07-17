"""Extração de texto de imagens com Amazon Textract.

Exemplo:
    python src/main.py assets/lista_material_escolar.png --region us-east-1
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def analisar_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extrai texto de uma imagem usando o Amazon Textract."
    )
    parser.add_argument(
        "imagem",
        type=Path,
        help="Caminho da imagem PNG ou JPEG que será analisada.",
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="Região AWS utilizada. Padrão: us-east-1.",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=Path("outputs"),
        help="Diretório dos arquivos gerados. Padrão: outputs.",
    )
    return parser.parse_args()


def extrair_linhas(resposta: dict[str, Any]) -> list[str]:
    """Seleciona os blocos de texto classificados como linha."""
    linhas: list[str] = []

    for bloco in resposta.get("Blocks", []):
        if bloco.get("BlockType") == "LINE" and bloco.get("Text"):
            linhas.append(str(bloco["Text"]))

    return linhas


def executar_ocr(imagem: Path, regiao: str) -> dict[str, Any]:
    """Envia os bytes da imagem ao Amazon Textract."""
    if not imagem.exists():
        raise FileNotFoundError(f"Imagem não encontrada: {imagem}")

    if imagem.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        raise ValueError("Formato inválido. Utilize uma imagem PNG ou JPEG.")

    try:
        import boto3
    except ModuleNotFoundError as erro:
        raise RuntimeError(
            "Dependência boto3 não instalada. Execute: pip install -r requirements.txt"
        ) from erro

    cliente = boto3.client("textract", region_name=regiao)

    with imagem.open("rb") as arquivo:
        conteudo = arquivo.read()

    return cliente.detect_document_text(Document={"Bytes": conteudo})


def salvar_resultados(
    resposta: dict[str, Any],
    linhas: list[str],
    diretorio: Path,
    nome_base: str,
) -> tuple[Path, Path]:
    """Salva a resposta completa em JSON e o texto reconhecido em TXT."""
    diretorio.mkdir(parents=True, exist_ok=True)

    caminho_json = diretorio / f"{nome_base}_response.json"
    caminho_txt = diretorio / f"{nome_base}_texto.txt"

    with caminho_json.open("w", encoding="utf-8") as arquivo_json:
        json.dump(
            resposta,
            arquivo_json,
            ensure_ascii=False,
            indent=2,
            default=str,
        )

    with caminho_txt.open("w", encoding="utf-8") as arquivo_txt:
        arquivo_txt.write("\n".join(linhas))

    return caminho_json, caminho_txt


def main() -> int:
    args = analisar_argumentos()

    try:
        resposta = executar_ocr(args.imagem, args.region)
        linhas = extrair_linhas(resposta)
        caminho_json, caminho_txt = salvar_resultados(
            resposta=resposta,
            linhas=linhas,
            diretorio=args.saida,
            nome_base=args.imagem.stem,
        )

        print("\nTexto identificado pelo Amazon Textract:\n")

        if linhas:
            for numero, linha in enumerate(linhas, start=1):
                print(f"{numero:02d}. {linha}")
        else:
            print("Nenhuma linha de texto foi identificada.")

        print(f"\nResposta JSON salva em: {caminho_json}")
        print(f"Texto extraído salvo em: {caminho_txt}")
        return 0

    except FileNotFoundError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
    except ValueError as erro:
        print(f"Erro de validação: {erro}", file=sys.stderr)
    except RuntimeError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
    except Exception as erro:
        nome = type(erro).__name__
        print(f"Falha ao processar a imagem ({nome}): {erro}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
