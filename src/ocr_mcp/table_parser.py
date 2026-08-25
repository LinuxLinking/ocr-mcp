"""
Table Parser - 表格识别和解析
负责识别图片中的表格并转换为结构化数据
"""

from typing import Any

import cv2
import numpy as np

from .ocr_engine import OCREngine


class TableParser:
    """表格识别解析器 - 独立实例，支持并行"""

    def __init__(self):
        # 使用独立的 OCR 引擎实例
        self.ocr_engine = OCREngine()

    def recognize_table(
        self, image: np.ndarray, language: str = "ch"
    ) -> list[list[str]]:
        """
        识别图片中的表格

        Args:
            image: 图片数据
            language: 语言代码

        Returns:
            二维列表，表示表格数据
        """
        # 使用 OCR 引擎识别文字及位置
        cells = self.ocr_engine.get_boxes(image, language=language, use_angle_cls=True)

        if not cells:
            return []

        # 按 Y 坐标排序，分行
        cells.sort(key=lambda c: (c["y"], c["x"]))

        # 使用聚类算法分行
        rows = self._cluster_rows(cells)

        return rows

    def _cluster_rows(self, cells: list[dict]) -> list[list[str]]:
        """
        将单元格按 Y 坐标聚类成行

        Args:
            cells: 单元格列表，每个包含 text, x, y

        Returns:
            二维列表
        """
        if not cells:
            return []

        # 计算平均高度，用于确定行间距阈值
        y_values = [c["y"] for c in cells]
        if len(y_values) > 1:
            y_diffs = [y_values[i+1] - y_values[i] for i in range(len(y_values)-1)]
            avg_diff = sum(y_diffs) / len(y_diffs)
            y_threshold = avg_diff * 0.5
        else:
            y_threshold = 20

        # 分行
        rows = []
        current_row = [cells[0]]

        for cell in cells[1:]:
            if abs(cell["y"] - current_row[-1]["y"]) < y_threshold:
                current_row.append(cell)
            else:
                # 按 X 坐标排序当前行
                current_row.sort(key=lambda c: c["x"])
                rows.append([c["text"] for c in current_row])
                current_row = [cell]

        # 处理最后一行
        if current_row:
            current_row.sort(key=lambda c: c["x"])
            rows.append([c["text"] for c in current_row])

        return rows

    def format_table(self, table_data: list[list[str]]) -> str:
        """
        格式化表格数据为文本

        Args:
            table_data: 二维列表

        Returns:
            格式化的表格字符串
        """
        if not table_data:
            return "空表格"

        # 计算每列的最大宽度
        col_widths = []
        for row in table_data:
            for i, cell in enumerate(row):
                # 中文字符占两个宽度
                width = sum(2 if ord(c) > 127 else 1 for c in cell)
                if i >= len(col_widths):
                    col_widths.append(width)
                else:
                    col_widths[i] = max(col_widths[i], width)

        # 构建分隔线
        separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

        # 构建表格
        lines = [separator]
        for row in table_data:
            row_str = "|"
            for i, cell in enumerate(row):
                # 补齐宽度
                width = sum(2 if ord(c) > 127 else 1 for c in cell)
                padding = col_widths[i] - width if i < len(col_widths) else 0
                row_str += f" {cell}{' ' * padding} |"
            lines.append(row_str)
            lines.append(separator)

        return "\n".join(lines)
