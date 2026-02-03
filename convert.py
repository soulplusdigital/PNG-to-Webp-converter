#!/usr/bin/env python3
"""
PNG to WebP Converter
Script de linha de comando para converter imagens PNG para WebP.

Uso:
    python convert.py imagem.png
    python convert.py ./imagens/
    python convert.py ./imagens/ -o ./webp/ -q 90 -r

Para mais informações:
    python convert.py --help
"""

import sys
import argparse
from pathlib import Path

from src.converter import convert_png_to_webp, convert_directory, format_size


def main():
    parser = argparse.ArgumentParser(
        description='Converte imagens PNG para WebP com compressão otimizada',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python convert.py imagem.png                       # Converte um arquivo
  python convert.py ./imagens/                       # Converte diretório
  python convert.py ./imagens/ -o ./webp/ -q 90     # Saída separada, qualidade 90
  python convert.py ./imagens/ -r                    # Recursivo (subpastas)
  python convert.py ./public/img/ -o ./public/webp/ -q 85 -r

Recomendações de qualidade:
  70-80  → Thumbnails e imagens pequenas
  80-85  → Web geral (recomendado)
  85-90  → E-commerce, fotos de produtos
  90-95  → Ícones, logos, detalhes finos
        """
    )
    
    parser.add_argument(
        'input', 
        help='Arquivo PNG ou diretório contendo arquivos PNG'
    )
    parser.add_argument(
        '-o', '--output', 
        help='Arquivo ou diretório de saída (padrão: mesmo local do original)'
    )
    parser.add_argument(
        '-q', '--quality', 
        type=int, 
        default=85,
        help='Qualidade da compressão, 1-100 (padrão: 85)'
    )
    parser.add_argument(
        '-r', '--recursive', 
        action='store_true',
        help='Processa subdiretórios recursivamente'
    )
    
    args = parser.parse_args()
    
    # Validação da qualidade
    if args.quality < 1 or args.quality > 100:
        print("❌ Erro: Qualidade deve ser entre 1 e 100")
        sys.exit(1)
    
    input_path = Path(args.input)
    
    # Verifica se o caminho existe
    if not input_path.exists():
        print(f"❌ Erro: Caminho não encontrado: {args.input}")
        sys.exit(1)
    
    try:
        if input_path.is_file():
            # Converte arquivo único
            if input_path.suffix.lower() != '.png':
                print(f"❌ Erro: Arquivo não é PNG: {args.input}")
                sys.exit(1)
                
            result = convert_png_to_webp(args.input, args.output, args.quality)
            
            print(f"\n✓ Convertido com sucesso!")
            print(f"  Entrada:  {result['input']}")
            print(f"  Saída:    {result['output']}")
            print(f"  Tamanho:  {format_size(result['original_size'])} → {format_size(result['new_size'])}")
            print(f"  Redução:  {result['reduction_percent']}%\n")
            
        elif input_path.is_dir():
            # Converte diretório
            results = convert_directory(
                args.input, 
                args.output, 
                args.quality, 
                args.recursive
            )
            
            if not results:
                sys.exit(0)
                
            # Conta sucessos e erros
            success = sum(1 for r in results if 'error' not in r)
            errors = len(results) - success
            
            if errors > 0:
                print(f"⚠️  {errors} arquivo(s) com erro")
                
    except KeyboardInterrupt:
        print("\n\n⚠️  Conversão cancelada pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
