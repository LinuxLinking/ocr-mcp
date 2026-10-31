# OCR MCP Service

<!-- mcp-name: io.github.LinuxLinking/ocr-mcp -->

[中文](README.zh-CN.md) | [日本語](README.ja.md)

MCP service for OCR tasks powered by PaddleOCR.

## Features

- Text recognition from images
- Table recognition with simple structured output
- Handwriting recognition
- Formula recognition with LaTeX output
- Local file paths and HTTP/HTTPS URLs
- MCP stdio server for desktop or agent integrations

## Installation

### From PyPI

```bash
pip install ocr-mcp
```

### From source

```bash
git clone https://github.com/LinuxLinking/OCR_MCP.git
cd OCR_MCP
pip install -e .
```

## Usage

Run the MCP server:

```bash
ocr-mcp
```

Or:

```bash
python -m ocr_mcp
```

## Claude Desktop

Add this to your Claude Desktop config:

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

## Tools

### `ocr_recognize`

Recognize text in an image.

- `source` required, local path or URL
- `language` optional, default `ch`, supports `ch`, `en`, `japan`, `korean`
- `use_angle_cls` optional, default `true`

### `ocr_table`

Recognize a table and return a text table.

- `source` required, local path or URL
- `language` optional, default `ch`

### `ocr_handwrite`

Recognize handwriting in an image.

- `source` required, local path or URL
- `language` optional, default `ch`

### `ocr_formula`

Recognize formulas and return LaTeX.

- `source` required, local path or URL

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Project Layout

```text
src/ocr_mcp/
  __init__.py
  __main__.py
  server.py
  ocr_engine.py
  table_parser.py
  formula_engine.py
  utils.py
tests/
pyproject.toml
LICENSE
README.md
```

## Dependencies

- PaddleOCR
- PaddlePaddle
- OpenCV
- MCP

## License

MIT. See [LICENSE](LICENSE).

## Related

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Model Context Protocol](https://modelcontextprotocol.io/)
