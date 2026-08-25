"""
OCR MCP Server - MCP 服务主入口
提供 OCR 文字识别和表格识别功能
"""

import asyncio
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from .ocr_engine import OCREngine
from .table_parser import TableParser
from .formula_engine import FormulaEngine


# 工厂函数：每次调用创建独立实例
def create_ocr_engine():
    """创建独立的 OCR 引擎实例"""
    return OCREngine()

def create_table_parser():
    """创建独立的表格解析器实例"""
    return TableParser()

def create_formula_engine():
    """创建独立的公式识别引擎实例"""
    return FormulaEngine()


async def handle_list_tools(
    ctx: Any, params: Any
) -> types.ListToolsResult:
    """列出可用的工具"""
    return types.ListToolsResult(
        tools=[
            types.Tool(
                name="ocr_recognize",
                description="识别图片中的文字内容。支持本地文件路径或 URL。",
                input_schema={
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "图片来源：本地文件路径或 URL",
                        },
                        "language": {
                            "type": "string",
                            "description": "识别语言，默认 'ch'（中文）。可选：ch/en/japan/korean 等",
                            "default": "ch",
                        },
                        "use_angle_cls": {
                            "type": "boolean",
                            "description": "是否启用文字方向分类，默认 true",
                            "default": True,
                        },
                    },
                    "required": ["source"],
                },
            ),
            types.Tool(
                name="ocr_table",
                description="识别图片中的表格内容，返回结构化的表格数据。",
                input_schema={
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "图片来源：本地文件路径或 URL",
                        },
                        "language": {
                            "type": "string",
                            "description": "识别语言，默认 'ch'（中文）",
                            "default": "ch",
                        },
                    },
                    "required": ["source"],
                },
            ),
            types.Tool(
                name="ocr_handwrite",
                description="识别图片中的手写文字内容。",
                input_schema={
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "图片来源：本地文件路径或 URL",
                        },
                        "language": {
                            "type": "string",
                            "description": "识别语言，默认 'ch'（中文）",
                            "default": "ch",
                        },
                    },
                    "required": ["source"],
                },
            ),
            types.Tool(
                name="ocr_formula",
                description="识别图片中的数学公式，返回 LaTeX 格式。",
                input_schema={
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "图片来源：本地文件路径或 URL",
                        },
                    },
                    "required": ["source"],
                },
            ),
        ]
    )


async def handle_call_tool(
    ctx: Any, params: types.CallToolRequestParams
) -> types.CallToolResult:
    """处理工具调用"""
    try:
        name = params.name
        arguments = params.arguments or {}

        if name == "ocr_recognize":
            result = await ocr_recognize(
                source=arguments["source"],
                language=arguments.get("language", "ch"),
                use_angle_cls=arguments.get("use_angle_cls", True),
            )
        elif name == "ocr_table":
            result = await ocr_table(
                source=arguments["source"],
                language=arguments.get("language", "ch"),
            )
        elif name == "ocr_handwrite":
            result = await ocr_handwrite(
                source=arguments["source"],
                language=arguments.get("language", "ch"),
            )
        elif name == "ocr_formula":
            result = await ocr_formula(
                source=arguments["source"],
            )
        else:
            result = f"未知工具: {name}"

        return types.CallToolResult(
            content=[types.TextContent(type="text", text=result)]
        )

    except Exception as e:
        error_msg = f"OCR 处理失败: {str(e)}"
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=error_msg)],
            is_error=True,
        )


async def ocr_recognize(
    source: str, language: str = "ch", use_angle_cls: bool = True
) -> str:
    """执行 OCR 文字识别"""
    try:
        # 创建独立的 OCR 引擎实例
        ocr_engine = create_ocr_engine()

        # 获取图片（本地路径或 URL）
        image = ocr_engine.load_image(source)

        # 执行 OCR
        results = ocr_engine.recognize(
            image, language=language, use_angle_cls=use_angle_cls
        )

        if not results:
            return "未识别到任何文字内容"

        # 格式化输出
        output_lines = []
        for i, (text, confidence) in enumerate(results, 1):
            output_lines.append(f"{i}. {text} (置信度: {confidence:.2%})")

        return "\n".join(output_lines)

    except Exception as e:
        raise RuntimeError(f"OCR 识别失败: {str(e)}")


async def ocr_table(source: str, language: str = "ch") -> str:
    """执行表格识别"""
    try:
        # 创建独立的表格解析器实例
        table_parser = create_table_parser()

        # 获取图片
        image = table_parser.ocr_engine.load_image(source)

        # 识别表格
        table_data = table_parser.recognize_table(
            image, language=language
        )

        if not table_data:
            return "未识别到表格内容"

        # 格式化表格输出
        return table_parser.format_table(table_data)

    except Exception as e:
        raise RuntimeError(f"表格识别失败: {str(e)}")


async def ocr_handwrite(source: str, language: str = "ch") -> str:
    """执行手写体识别"""
    try:
        # 创建独立的 OCR 引擎实例
        ocr_engine = create_ocr_engine()

        # 获取图片
        image = ocr_engine.load_image(source)

        # 执行手写体识别
        results = ocr_engine.recognize(
            image, language=language, use_angle_cls=True
        )

        if not results:
            return "未识别到任何手写文字"

        # 格式化输出
        output_lines = []
        for i, (text, confidence) in enumerate(results, 1):
            output_lines.append(f"{i}. {text} (置信度: {confidence:.2%})")

        return "\n".join(output_lines)

    except Exception as e:
        raise RuntimeError(f"手写体识别失败: {str(e)}")


async def ocr_formula(source: str) -> str:
    """执行公式识别"""
    try:
        # 创建独立的公式识别引擎实例
        formula_engine = create_formula_engine()

        # 获取图片
        ocr_engine = create_ocr_engine()
        image = ocr_engine.load_image(source)

        # 识别公式
        formulas = formula_engine.recognize_formula(image)

        if not formulas:
            return "未识别到任何数学公式"

        # 格式化输出
        output_lines = []
        for i, item in enumerate(formulas, 1):
            latex = item.get('latex', '')
            output_lines.append(f"公式 {i}:")
            output_lines.append(f"  LaTeX: {latex}")

        return "\n".join(output_lines)

    except Exception as e:
        raise RuntimeError(f"公式识别失败: {str(e)}")


# 创建 MCP 服务实例（MCP 2.0 用构造函数注册回调）
app = Server(
    "ocr-mcp",
    on_list_tools=handle_list_tools,
    on_call_tool=handle_call_tool,
)


async def run_server():
    """运行 MCP 服务器"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main():
    """主入口函数"""
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nOCR MCP 服务已停止", file=sys.stderr)
    except Exception as e:
        print(f"服务启动失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
