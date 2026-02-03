"""
Módulo de conversão PNG para WebP.
Funções para converter imagens individuais ou em lote.
"""

from pathlib import Path
from PIL import Image


def convert_png_to_webp(input_path: str, output_path: str = None, quality: int = 85) -> dict:
    """
    Converte uma imagem PNG para WebP.
    
    Args:
        input_path: Caminho da imagem PNG
        output_path: Caminho de saída (opcional, usa mesmo nome com .webp)
        quality: Qualidade da compressão (1-100, default: 85)
    
    Returns:
        Dict com informações da conversão:
        - input: caminho original
        - output: caminho do arquivo gerado
        - original_size: tamanho original em bytes
        - new_size: tamanho do WebP em bytes
        - reduction_percent: percentual de redução
    
    Raises:
        FileNotFoundError: Se o arquivo não existir
        ValueError: Se o arquivo não for PNG
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")
    
    if input_file.suffix.lower() != '.png':
        raise ValueError(f"Arquivo não é PNG: {input_path}")
    
    if output_path is None:
        output_path = input_file.with_suffix('.webp')
    else:
        output_path = Path(output_path)
    
    original_size = input_file.stat().st_size
    
    with Image.open(input_file) as img:
        # Preserva transparência se existir
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img.save(output_path, 'WEBP', quality=quality, lossless=False)
        else:
            img = img.convert('RGB')
            img.save(output_path, 'WEBP', quality=quality, lossless=False)
    
    new_size = Path(output_path).stat().st_size
    reduction = ((original_size - new_size) / original_size) * 100
    
    return {
        'input': str(input_file),
        'output': str(output_path),
        'original_size': original_size,
        'new_size': new_size,
        'reduction_percent': round(reduction, 1)
    }


def convert_directory(
    input_dir: str, 
    output_dir: str = None, 
    quality: int = 85, 
    recursive: bool = False,
    verbose: bool = True
) -> list:
    """
    Converte todas as imagens PNG em um diretório.
    
    Args:
        input_dir: Diretório com as imagens PNG
        output_dir: Diretório de saída (opcional, usa o mesmo)
        quality: Qualidade da compressão (1-100)
        recursive: Se True, processa subdiretórios
        verbose: Se True, imprime progresso
    
    Returns:
        Lista com resultados de cada conversão
    
    Raises:
        NotADirectoryError: Se input_dir não for um diretório
    """
    input_path = Path(input_dir)
    
    if not input_path.is_dir():
        raise NotADirectoryError(f"Não é um diretório: {input_dir}")
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path
    
    pattern = '**/*.png' if recursive else '*.png'
    png_files = list(input_path.glob(pattern))
    
    if not png_files:
        if verbose:
            print(f"Nenhum arquivo PNG encontrado em: {input_dir}")
        return []
    
    results = []
    total_original = 0
    total_new = 0
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Convertendo {len(png_files)} arquivo(s) PNG para WebP")
        print(f"Qualidade: {quality}%")
        print(f"{'='*60}\n")
    
    for png_file in png_files:
        try:
            if output_dir:
                relative = png_file.relative_to(input_path)
                out_file = output_path / relative.with_suffix('.webp')
                out_file.parent.mkdir(parents=True, exist_ok=True)
            else:
                out_file = None
            
            result = convert_png_to_webp(
                str(png_file), 
                str(out_file) if out_file else None, 
                quality
            )
            results.append(result)
            
            total_original += result['original_size']
            total_new += result['new_size']
            
            if verbose:
                print(f"✓ {png_file.name}")
                print(f"  {format_size(result['original_size'])} → {format_size(result['new_size'])} "
                      f"(-{result['reduction_percent']}%)")
            
        except Exception as e:
            if verbose:
                print(f"✗ {png_file.name}: {e}")
            results.append({'input': str(png_file), 'error': str(e)})
    
    if verbose and total_original > 0:
        total_reduction = ((total_original - total_new) / total_original) * 100
        print(f"\n{'='*60}")
        print(f"TOTAL: {format_size(total_original)} → {format_size(total_new)}")
        print(f"Redução total: {total_reduction:.1f}%")
        print(f"Economia: {format_size(total_original - total_new)}")
        print(f"{'='*60}\n")
    
    return results


def format_size(size_bytes: int) -> str:
    """
    Formata tamanho em bytes para formato legível.
    
    Args:
        size_bytes: Tamanho em bytes
    
    Returns:
        String formatada (ex: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
