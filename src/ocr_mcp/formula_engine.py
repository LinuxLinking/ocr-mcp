"""
Formula Engine - 公式识别
负责识别图片中的数学公式并转换为 LaTeX
"""

import os
from pathlib import Path
from typing import Optional

import cv2
import numpy as np


class FormulaEngine:
    """公式识别引擎 - 基于 PaddleOCR PP-Structure"""

    def __init__(self):
        self._engine = None

    def _init_engine(self):
        """初始化 PP-Structure 引擎"""
        if self._engine is None:
            from paddleocr import PPStructure
            self._engine = PPStructure(
                table=True,
                ocr=True,
                layout=True,
                formula=True,
            )

    def recognize_formula(
        self,
        image: np.ndarray,
    ) -> list[dict]:
        """
        识别图片中的数学公式

        Args:
            image: 图片数据 (numpy array)

        Returns:
            list of dict: 每个公式包含 latex 和 region 信息
        """
        self._init_engine()
        result = self._engine(image)

        formulas = []
        for item in result:
            # 检查是否是公式类型
            if item.get('type') == 'equation':
                latex = item.get('res', {}).get('latex', '')
                if latex:
                    formulas.append({
                        'latex': latex,
                        'region': item.get('bbox', []),
                    })

        return formulas

    def recognize_all(
        self,
        image: np.ndarray,
    ) -> dict:
        """
        识别图片中的所有内容（文字 + 公式 + 表格）

        Args:
            image: 图片数据

        Returns:
            dict: 包含 texts, formulas, tables
        """
        self._init_engine()
        result = self._engine(image)

        output = {
            'texts': [],
            'formulas': [],
            'tables': [],
        }

        for item in result:
            item_type = item.get('type', '')

            if item_type == 'text':
                text_res = item.get('res', {})
                if isinstance(text_res, dict):
                    output['texts'].append({
                        'text': text_res.get('text', ''),
                        'confidence': text_res.get('confidence', 0),
                        'region': item.get('bbox', []),
                    })
                elif isinstance(text_res, str):
                    output['texts'].append({
                        'text': text_res,
                        'confidence': 1.0,
                        'region': item.get('bbox', []),
                    })

            elif item_type == 'equation':
                latex = item.get('res', {}).get('latex', '')
                if latex:
                    output['formulas'].append({
                        'latex': latex,
                        'region': item.get('bbox', []),
                    })

            elif item_type == 'table':
                table_html = item.get('res', {}).get('html', '')
                if table_html:
                    output['tables'].append({
                        'html': table_html,
                        'region': item.get('bbox', []),
                    })

        return output
