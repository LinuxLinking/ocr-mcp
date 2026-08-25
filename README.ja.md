# OCR MCP Service

[English](README.md) | [中文](README.zh-CN.md)

PaddleOCR を活用した MCP 文字認識サービスで、OCR 文字認識とテーブル認識機能をサポートしています。

## 機能

- **OCR 文字認識**：画像内のテキストコンテンツを認識し、中国語、英語、その他の言語をサポート
- **テーブル認識**：画像内のテーブルを認識し、構造化データを返す
- **手書き認識**：画像内の手書きテキストを認識
- **数式認識**：画像内の数式を認識し、LaTeX 形式で返す
- **マルチフォーマット対応**：JPG、PNG、BMP、TIFF、WebP などの画像形式をサポート
- **URL 対応**：ローカルファイルパスとネットワーク URL の両方をサポート
- **MCP プロトコル**：標準 MCP サービスで、MCP 対応 AI アシスタントに統合可能

## インストール

### pip でインストール

```bash
pip install ocr-mcp
```

### ソースからインストール

```bash
git clone https://github.com/LinuxLinking/OCR_MCP.git
cd OCR_MCP
pip install -e .
```

## 使用方法

### MCP サービスとして実行

```bash
# 直接実行
ocr-mcp

# Python モジュール経由で実行
python -m ocr_mcp
```

### Claude Desktop への統合

Claude Desktop の設定ファイルに追加：

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

### MCP ツールの説明

#### `ocr_recognize`

画像内のテキストコンテンツを認識します。

**パラメータ：**
- `source`（必須）：画像ソース、ローカルファイルパスまたは URL
- `language`（オプション）：認識言語、デフォルト `ch`（中国語）、`en`、`japan`、`korean` などをサポート
- `use_angle_cls`（オプション）：テキスト方向分類を有効にするかどうか、デフォルト `true`

**出力例：**
```
1. こんにちは世界 (信頼度: 98.50%)
2. Hello World (信頼度: 97.20%)
```

#### `ocr_table`

画像内のテーブルコンテンツを認識し、構造化データを返します。

**パラメータ：**
- `source`（必須）：画像ソース、ローカルファイルパスまたは URL
- `language`（オプション）：認識言語、デフォルト `ch`

**出力例：**
```
+--------+-----+------+
| 名前   | 年齢 | 都市 |
+--------+-----+------+
| 田中   | 25  | 東京 |
+--------+-----+------+
| 佐藤   | 30  | 大阪 |
+--------+-----+------+
```

#### `ocr_handwrite`

画像内の手書きテキストコンテンツを認識します。

**パラメータ：**
- `source`（必須）：画像ソース、ローカルファイルパスまたは URL
- `language`（オプション）：認識言語、デフォルト `ch`

**出力例：**
```
1. こんにちは世界 (信頼度: 85.50%)
2. Hello (信頼度: 82.30%)
```

#### `ocr_formula`

画像内の数式を認識し、LaTeX 形式で返します。

**パラメータ：**
- `source`（必須）：画像ソース、ローカルファイルパスまたは URL

**出力例：**
```
数式 1:
  LaTeX: E = mc^2
数式 2:
  LaTeX: \int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
```

## 開発

### 開発依存関係のインストール

```bash
pip install -e ".[dev]"
```

### テストの実行

```bash
pytest tests/ -v
```

## プロジェクト構造

```
OCR_MCP/
├── src/ocr_mcp/
│   ├── __init__.py          # パッケージ初期化
│   ├── __main__.py          # モジュールエントリポイント
│   ├── server.py            # MCP サービスメインエントリ（ディスパッチ層）
│   ├── ocr_engine.py        # サブプログラム 1：テキスト認識エンジン
│   ├── table_parser.py      # サブプログラム 2：テーブル認識エンジン
│   ├── formula_engine.py    # サブプログラム 3：数式認識エンジン
│   └── utils.py             # ユーティリティ関数
├── tests/
│   └── test_ocr.py          # テストファイル
├── pyproject.toml           # プロジェクト設定
├── LICENSE                  # MIT ライセンス
└── README.md                # プロジェクトドキュメント
```

## アーキテクチャ

このプロジェクトは**サブプログラム並列アーキテクチャ**を採用しており、4 つの認識ツールが独立して個別に呼び出し可能です：

```
┌─────────────────────────────────────────────────────────┐
│                   MCP Server (ディスパッチ層)              │
├──────────────┬──────────────┬─────────────┬─────────────┤
│サブプログラム1│サブプログラム2│サブプログラム3│サブプログラム4│
│ocr_recognize │  ocr_table   │ocr_handwrite│ ocr_formula │
│テキスト認識  │テーブル認識  │ 手書き認識   │  数式認識   │
└──────────────┴──────────────┴─────────────┴─────────────┘
       ↓              ↓              ↓              ↓
   OCREngine     TableParser    OCREngine    FormulaEngine
```

**特徴：**
- 各サブプログラムが独立して実行され、相互依存なし
- 並列呼び出しをサポートし、複数のタスクを同時処理可能
- 各呼び出しで独立したインスタンスを作成し、状態の競合を回避
- 任意のサブプログラムを個別に拡張または置換可能

## 依存関係

- **PaddleOCR**：OCR 認識コアエンジン
- **PaddlePaddle**：深層学習フレームワーク
- **OpenCV**：画像処理
- **MCP**：Model Context Protocol サービスフレームワーク

## ライセンス

このプロジェクトは [MIT ライセンス](LICENSE) の下でオープンソースとして公開されています。

## 関連リンク

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Model Context Protocol](https://modelcontextprotocol.io/)
