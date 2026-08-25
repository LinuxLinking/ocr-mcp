# OCR MCP サービス

[English](README.md) | [中文](README.zh-CN.md)

PaddleOCR を使った MCP ベースの OCR サービスです。文字認識、表認識、手書き認識、数式認識を提供します。

## 機能

- 画像内の文字認識
- 表の認識と簡易な構造化出力
- 手書き文字の認識
- 数式認識と LaTeX 出力
- ローカルパスと HTTP/HTTPS URL に対応
- stdio 経由の MCP サーバー

## インストール

### PyPI から

```bash
pip install ocr-mcp
```

### ソースから

```bash
git clone https://github.com/LinuxLinking/OCR_MCP.git
cd OCR_MCP
pip install -e .
```

## 使い方

MCP サーバーを起動します。

```bash
ocr-mcp
```

または:

```bash
python -m ocr_mcp
```

## Claude Desktop

Claude Desktop の設定に次を追加します。

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

## ツール

### `ocr_recognize`

画像内の文字を認識します。

- `source` 必須。ローカルパスまたは URL
- `language` 任意。既定は `ch`。`ch`、`en`、`japan`、`korean` をサポート
- `use_angle_cls` 任意。既定は `true`

### `ocr_table`

表を認識してテキスト表として返します。

- `source` 必須。ローカルパスまたは URL
- `language` 任意。既定は `ch`

### `ocr_handwrite`

画像内の手書きを認識します。

- `source` 必須。ローカルパスまたは URL
- `language` 任意。既定は `ch`

### `ocr_formula`

数式を認識して LaTeX を返します。

- `source` 必須。ローカルパスまたは URL

## 開発

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## プロジェクト構成

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

## 依存関係

- PaddleOCR
- PaddlePaddle
- OpenCV
- MCP

## ライセンス

MIT。詳細は [LICENSE](LICENSE) を参照してください。

## 関連リンク

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Model Context Protocol](https://modelcontextprotocol.io/)
