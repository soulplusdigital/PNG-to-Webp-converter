# PNG to WebP Converter

Ferramenta de linha de comando para converter imagens PNG para WebP com compressão otimizada.

## 🚀 Recursos

- Conversão individual ou em lote de arquivos PNG
- Processamento recursivo de subdiretórios
- Controle de qualidade de compressão (1-100)
- Preservação de transparência (canal alpha)
- Relatório detalhado de economia de espaço
- Saída para diretório customizado

## 📋 Requisitos

- Python 3.8+
- Pillow

## 🔧 Instalação

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/soulplusdigital/PNG-to-Webp-converter.git
cd PNG-to-Webp-converter
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 📖 Uso

### Converter um único arquivo

```bash
python convert.py imagem.png
```

### Converter todos os PNGs de um diretório

```bash
python convert.py ./imagens/
```

### Converter recursivamente (incluindo subpastas)

```bash
python convert.py ./imagens/ -r
```

### Especificar diretório de saída

```bash
python convert.py ./imagens/ -o ./webp/
```

### Definir qualidade de compressão

```bash
# Qualidade 90% (maior qualidade, menor compressão)
python convert.py ./imagens/ -q 90

# Qualidade 70% (menor qualidade, maior compressão)
python convert.py ./imagens/ -q 70
```

### Combinando opções

```bash
python convert.py ./public/images/ -o ./public/webp/ -q 85 -r
```

## ⚙️ Opções

| Opção             | Descrição                         | Padrão        |
| ----------------- | --------------------------------- | ------------- |
| `input`           | Arquivo PNG ou diretório com PNGs | (obrigatório) |
| `-o, --output`    | Arquivo ou diretório de saída     | Mesmo local   |
| `-q, --quality`   | Qualidade da compressão (1-100)   | 85            |
| `-r, --recursive` | Processa subdiretórios            | False         |
| `-h, --help`      | Exibe ajuda                       | -             |

## 📊 Exemplo de Saída

```
============================================================
Convertendo 5 arquivo(s) PNG para WebP
Qualidade: 85%
============================================================

✓ hero-banner.png
  1.2 MB → 245.3 KB (-79.8%)
✓ logo.png
  89.5 KB → 32.1 KB (-64.1%)
✓ icon-menu.png
  12.3 KB → 4.8 KB (-61.0%)
✓ background.png
  2.4 MB → 512.7 KB (-78.6%)
✓ product-photo.png
  856.2 KB → 198.4 KB (-76.8%)

============================================================
TOTAL: 4.5 MB → 993.3 KB
Redução total: 78.2%
Economia: 3.5 MB
============================================================
```

## 🎯 Recomendações de Qualidade

| Uso          | Qualidade | Descrição                            |
| ------------ | --------- | ------------------------------------ |
| Web (geral)  | 80-85     | Melhor equilíbrio qualidade/tamanho  |
| E-commerce   | 85-90     | Boa qualidade para fotos de produtos |
| Ícones/logos | 90-95     | Preserva detalhes finos              |
| Thumbnails   | 70-80     | Imagens pequenas, prioriza tamanho   |
| Arquivamento | 95-100    | Máxima qualidade                     |

## 🔄 Integração com Next.js

Após converter suas imagens, atualize as referências no seu projeto:

```jsx
// Antes
<Image src="/images/hero.png" ... />

// Depois
<Image src="/images/hero.webp" ... />
```

Ou use o componente `next/image` com formato automático:

```jsx
// next.config.js
module.exports = {
  images: {
    formats: ["image/webp"],
  },
};
```

## 📁 Estrutura do Projeto

```
png-to-webp-converter/
├── README.md
├── requirements.txt
├── .gitignore
├── convert.py          # Script principal (entrada)
├── src/
│   ├── __init__.py
│   └── converter.py    # Módulo de conversão
└── examples/
    ├── input/          # Coloque PNGs aqui para testar
    └── output/         # Resultados WebP
```

## 🤝 Uso como Módulo

Você também pode importar as funções em outros scripts:

```python
from src.converter import convert_png_to_webp, convert_directory

# Converter um arquivo
result = convert_png_to_webp('imagem.png', quality=85)
print(f"Redução: {result['reduction_percent']}%")

# Converter diretório
results = convert_directory('./imagens/', quality=90, recursive=True)
```

## 📄 Licença

MIT License - use livremente em projetos pessoais e comerciais.

---

Desenvolvido para otimização de performance web 🚀
