# OCR MCP 服务

[English](README.md) | [日本語](README.ja.md)

这是一个基于 PaddleOCR 的 MCP OCR 服务，提供文本识别、表格识别、手写识别和公式识别。

## 功能

- 图片文字识别
- 表格识别并输出简单结构化结果
- 手写体识别
- 数学公式识别并输出 LaTeX
- 支持本地路径和 HTTP/HTTPS URL
- 通过 stdio 提供 MCP 服务

## 安装

### 通过 pip 安装

```bash
pip install ocr-mcp
```

### 从源码安装

```bash
git clone https://github.com/LinuxLinking/OCR_MCP.git
cd OCR_MCP
pip install -e .
```

## 使用

启动 MCP 服务：

```bash
ocr-mcp
```

或：

```bash
python -m ocr_mcp
```

## Claude Desktop 配置

把下面内容加入 Claude Desktop 配置文件：

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

## 工具说明

### `ocr_recognize`

识别图片中的文本。

- `source` 必填，本地路径或 URL
- `language` 可选，默认 `ch`，支持 `ch`、`en`、`japan`、`korean`
- `use_angle_cls` 可选，默认 `true`

### `ocr_table`

识别表格并返回文本表格。

- `source` 必填，本地路径或 URL
- `language` 可选，默认 `ch`

### `ocr_handwrite`

识别图片中的手写内容。

- `source` 必填，本地路径或 URL
- `language` 可选，默认 `ch`

### `ocr_formula`

识别公式并返回 LaTeX。

- `source` 必填，本地路径或 URL

## 开发

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## 项目结构

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

## 依赖

- PaddleOCR
- PaddlePaddle
- OpenCV
- MCP

## 许可证

MIT，见 [LICENSE](LICENSE)。

## 相关链接

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Model Context Protocol](https://modelcontextprotocol.io/)
