# OCR MCP Service

[中文](README.zh-CN.md) | [日本語](README.ja.md)

MCP-based OCR service powered by PaddleOCR, supporting text recognition and table recognition.

## Features

- **OCR Text Recognition**: Recognize text content in images, supporting Chinese, English, and other languages
- **Table Recognition**: Recognize tables in images and return structured data
- **Handwriting Recognition**: Recognize handwritten text in images
- **Formula Recognition**: Recognize mathematical formulas in images and return LaTeX format
- **Multi-format Support**: Support JPG, PNG, BMP, TIFF, WebP and other image formats
- **URL Support**: Support both local file paths and network URLs
- **MCP Protocol**: Standard MCP service, can be integrated into MCP-compatible AI assistants

## Installation

### Install via pip

```bash
pip install ocr-mcp
```

### Install from source

```bash
git clone https://github.com/LinuxLinking/OCR_MCP.git
cd OCR_MCP
pip install -e .
```

## Usage

### Run as MCP service

```bash
# Run directly
ocr-mcp

# Or run via Python module
python -m ocr_mcp
```

### Integrate with Claude Desktop

Add to Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "ocr": {
      "command": "ocr-mcp",
      "args": []
    }
  }
}
```

### MCP Tool Description

#### `ocr_recognize`

Recognize text content in images.

**Parameters:**
- `source` (required): Image source, local file path or URL
- `language` (optional): Recognition language, default `ch` (Chinese), supports `en`, `japan`, `korean`, etc.
- `use_angle_cls` (optional): Whether to enable text direction classification, default `true`

**Example output:**
```
1. Hello World (confidence: 98.50%)
2. 你好世界 (confidence: 97.20%)
```

#### `ocr_table`

Recognize table content in images and return structured data.

**Parameters:**
- `source` (required): Image source, local file path or URL
- `language` (optional): Recognition language, default `ch`

**Example output:**
```
+--------+-----+------+
| Name   | Age | City |
+--------+-----+------+
| Alice  | 25  | NYC  |
+--------+-----+------+
| Bob    | 30  | LA   |
+--------+-----+------+
```

#### `ocr_handwrite`

Recognize handwritten text content in images.

**Parameters:**
- `source` (required): Image source, local file path or URL
- `language` (optional): Recognition language, default `ch`

**Example output:**
```
1. Hello World (confidence: 85.50%)
2. 你好 (confidence: 82.30%)
```

#### `ocr_formula`

Recognize mathematical formulas in images and return LaTeX format.

**Parameters:**
- `source` (required): Image source, local file path or URL

**Example output:**
```
Formula 1:
  LaTeX: E = mc^2
Formula 2:
  LaTeX: \int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
```

## Development

### Install development dependencies

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest tests/ -v
```

## Project Structure

```
OCR_MCP/
├── src/ocr_mcp/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Module entry point
│   ├── server.py            # MCP service main entry (dispatch layer)
│   ├── ocr_engine.py        # Subprogram 1: Text recognition engine
│   ├── table_parser.py      # Subprogram 2: Table recognition engine
│   ├── formula_engine.py    # Subprogram 3: Formula recognition engine
│   └── utils.py             # Utility functions
├── tests/
│   └── test_ocr.py          # Test files
├── pyproject.toml           # Project configuration
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

## Architecture

This project uses a **subprogram parallel architecture**, with 4 recognition tools that are independent and can be called separately:

```
┌─────────────────────────────────────────────────────────┐
│                   MCP Server (Dispatch Layer)            │
├──────────────┬──────────────┬─────────────┬─────────────┤
│ Subprogram 1 │ Subprogram 2 │ Subprogram 3│ Subprogram 4│
│ocr_recognize │  ocr_table   │ocr_handwrite│ ocr_formula │
│Text Recognition│Table Recognition│Handwriting Recognition│Formula Recognition│
└──────────────┴──────────────┴─────────────┴─────────────┘
       ↓              ↓              ↓              ↓
   OCREngine     TableParser    OCREngine    FormulaEngine
```

**Features:**
- Each subprogram runs independently without dependencies
- Supports parallel calls, can process multiple tasks simultaneously
- Creates independent instances for each call to avoid state conflicts
- Can individually extend or replace any subprogram

## Dependencies

- **PaddleOCR**: Core OCR recognition engine
- **PaddlePaddle**: Deep learning framework
- **OpenCV**: Image processing
- **MCP**: Model Context Protocol service framework

## License

This project is open-sourced under the [MIT License](LICENSE).

## Related Links

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Model Context Protocol](https://modelcontextprotocol.io/)
