# OCR MCP Service

基于 PaddleOCR 的 MCP 文字识别服务，支持 OCR 文字识别和表格识别功能。

## 功能特性

- **OCR 文字识别**：识别图片中的文字内容，支持中英文等多种语言
- **表格识别**：识别图片中的表格，返回结构化数据
- **手写体识别**：识别图片中的手写文字
- **公式识别**：识别图片中的数学公式，返回 LaTeX 格式
- **多格式支持**：支持 JPG、PNG、BMP、TIFF、WebP 等图片格式
- **URL 支持**：支持本地文件路径和网络 URL
- **MCP 协议**：标准 MCP 服务，可集成到支持 MCP 的 AI 助手

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

## 使用方法

### 作为 MCP 服务运行

```bash
# 直接运行
ocr-mcp

# 或通过 Python 模块运行
python -m ocr_mcp
```

### 集成到 Claude Desktop

在 Claude Desktop 配置文件中添加：

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

### MCP 工具说明

#### `ocr_recognize`

识别图片中的文字内容。

**参数：**
- `source` (必填)：图片来源，本地文件路径或 URL
- `language` (可选)：识别语言，默认 `ch`（中文），支持 `en`、`japan`、`korean` 等
- `use_angle_cls` (可选)：是否启用文字方向分类，默认 `true`

**示例输出：**
```
1. 你好世界 (置信度: 98.50%)
2. Hello World (置信度: 97.20%)
```

#### `ocr_table`

识别图片中的表格内容，返回结构化数据。

**参数：**
- `source` (必填)：图片来源，本地文件路径或 URL
- `language` (可选)：识别语言，默认 `ch`

**示例输出：**
```
+--------+------+------+
| 姓名   | 年龄 | 城市 |
+--------+------+------+
| 张三   | 25   | 北京 |
+--------+------+------+
| 李四   | 30   | 上海 |
+--------+------+------+
```

#### `ocr_handwrite`

识别图片中的手写文字内容。

**参数：**
- `source` (必填)：图片来源，本地文件路径或 URL
- `language` (可选)：识别语言，默认 `ch`

**示例输出：**
```
1. 你好世界 (置信度: 85.50%)
2. Hello (置信度: 82.30%)
```

#### `ocr_formula`

识别图片中的数学公式，返回 LaTeX 格式。

**参数：**
- `source` (必填)：图片来源，本地文件路径或 URL

**示例输出：**
```
公式 1:
  LaTeX: E = mc^2
公式 2:
  LaTeX: \int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
```

## 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest tests/ -v
```

## 项目结构

```
OCR_MCP/
├── src/ocr_mcp/
│   ├── __init__.py          # 包初始化
│   ├── __main__.py          # 模块运行入口
│   ├── server.py            # MCP 服务主入口（调度层）
│   ├── ocr_engine.py        # 子程序 1：文字识别引擎
│   ├── table_parser.py      # 子程序 2：表格识别引擎
│   ├── formula_engine.py    # 子程序 3：公式识别引擎
│   └── utils.py             # 工具函数
├── tests/
│   └── test_ocr.py          # 测试文件
├── pyproject.toml           # 项目配置
├── LICENSE                  # MIT 许可证
└── README.md                # 项目说明
```

## 架构说明

本项目采用 **子程序并行架构**，4 个识别工具相互独立，可单独调用：

```
┌─────────────────────────────────────────────────────────┐
│                   MCP Server (调度层)                     │
├──────────────┬──────────────┬─────────────┬─────────────┤
│   子程序 1   │   子程序 2   │   子程序 3  │   子程序 4  │
│ ocr_recognize│  ocr_table   │ ocr_handwrite│ ocr_formula │
│   文字识别   │   表格识别   │   手写识别   │   公式识别  │
└──────────────┴──────────────┴─────────────┴─────────────┘
       ↓              ↓              ↓              ↓
   OCREngine     TableParser    OCREngine    FormulaEngine
```

**特点：**
- 每个子程序独立运行，互不依赖
- 支持并行调用，可同时处理多个任务
- 每次调用创建独立实例，避免状态冲突
- 可单独扩展或替换任意子程序

## 依赖说明

- **PaddleOCR**：OCR 识别核心引擎
- **PaddlePaddle**：深度学习框架
- **OpenCV**：图像处理
- **MCP**：Model Context Protocol 服务框架

## 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。

## 相关链接

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Model Context Protocol](https://modelcontextprotocol.io/)
