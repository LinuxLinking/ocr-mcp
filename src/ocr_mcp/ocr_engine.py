"""
OCR Engine - PaddleOCR 封装
负责图片加载和文字识别
"""

import os
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def _setup_cache_dirs():
    """将所有 PaddlePaddle / HuggingFace 缓存目录重定向到项目目录下，避免写 C 盘"""
    # 项目根目录: src/ocr_mcp/ocr_engine.py -> 项目根
    project_root = str(Path(__file__).resolve().parent.parent.parent)
    cache_base = os.path.join(project_root, ".paddle_cache")

    env_map = {
        "PADDLE_PDX_CACHE_HOME": cache_base,          # paddlex 缓存
        "PADDLE_HOME": cache_base,                     # paddle 模型缓存
        "PP_HOME": cache_base,                         # PaddlePaddle 缓存
        "PADDLE_MODEL_HOME": os.path.join(cache_base, "models"),
        "HF_HOME": os.path.join(cache_base, "hf"),     # HuggingFace 缓存
        "TRANSFORMERS_CACHE": os.path.join(cache_base, "hf"),
        "XDG_CACHE_HOME": cache_base,
    }
    for key, value in env_map.items():
        if key not in os.environ:  # 不覆盖用户已有的设置
            os.environ[key] = value


# 在任何 paddle/paddleocr 导入之前设置缓存目录
_setup_cache_dirs()

import cv2
import numpy as np
import requests
from PIL import Image


class OCREngine:
    """OCR 识别引擎 - 每个实例独立，支持并行"""

    def __init__(self):
        self._ocr_instance = None
        self._language = None
        self._use_angle_cls = None

    def _init_ocr(self, language: str = "ch", use_angle_cls: bool = True):
        """初始化 OCR 实例"""
        # 只有当配置变化时才重新初始化
        if (self._ocr_instance is None or
            self._language != language or
            self._use_angle_cls != use_angle_cls):

            from paddleocr import PaddleOCR
            self._ocr_instance = PaddleOCR(
                lang=language,
                use_textline_orientation=use_angle_cls,
            )
            self._language = language
            self._use_angle_cls = use_angle_cls

    def load_image(self, source: str) -> np.ndarray:
        """
        加载图片，支持本地路径和 URL

        Args:
            source: 图片来源（本地路径或 URL）

        Returns:
            numpy.ndarray: 图片数据
        """
        # 判断是 URL 还是本地路径
        parsed = urlparse(source)
        if parsed.scheme in ("http", "https"):
            return self._load_image_from_url(source)
        else:
            return self._load_image_from_path(source)

    def _load_image_from_path(self, path: str) -> np.ndarray:
        """从本地路径加载图片"""
        path = Path(path).resolve()

        if not path.exists():
            raise FileNotFoundError(f"图片文件不存在: {path}")

        if not path.is_file():
            raise ValueError(f"路径不是文件: {path}")

        # 检查文件扩展名
        valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}
        if path.suffix.lower() not in valid_extensions:
            raise ValueError(f"不支持的图片格式: {path.suffix}")

        # 使用 np.fromfile + imdecode 读取，避免中文路径问题
        image = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise RuntimeError(f"无法读取图片: {path}")

        return image

    def _load_image_from_url(self, url: str) -> np.ndarray:
        """从 URL 加载图片"""
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()

            # 将响应内容转换为 numpy 数组
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            if image is None:
                raise RuntimeError(f"无法解码图片: {url}")

            return image

        except requests.RequestException as e:
            raise RuntimeError(f"下载图片失败: {str(e)}")

    def recognize(
        self,
        image: np.ndarray,
        language: str = "ch",
        use_angle_cls: bool = True,
    ) -> list[tuple[str, float]]:
        """
        识别图片中的文字

        Args:
            image: 图片数据 (numpy array)
            language: 语言代码
            use_angle_cls: 是否使用方向分类

        Returns:
            list of (text, confidence) tuples
        """
        self._init_ocr(language, use_angle_cls)
        result = self._ocr_instance.predict(image)

        if not result:
            return []

        # 提取文字和置信度（适配 PaddleOCR 3.x 返回的 OCRResult）
        texts = []
        for res in result:
            # 检查是否是新的返回格式（对象属性）
            if hasattr(res, 'rec_texts') and hasattr(res, 'rec_scores'):
                rec_texts = res.rec_texts
                rec_scores = res.rec_scores
                for text, score in zip(rec_texts, rec_scores):
                    if isinstance(text, (list, tuple)):
                        text = text[0] if text else ""
                    texts.append((str(text), float(score)))
            # 兼容旧格式（字典）
            elif isinstance(res, dict) and 'rec_texts' in res and 'rec_scores' in res:
                rec_texts = res['rec_texts']
                rec_scores = res['rec_scores']
                for text, score in zip(rec_texts, rec_scores):
                    if isinstance(text, (list, tuple)):
                        text = text[0] if text else ""
                    texts.append((str(text), float(score)))

        return texts

    def get_boxes(
        self,
        image: np.ndarray,
        language: str = "ch",
        use_angle_cls: bool = True,
    ) -> list[dict]:
        """
        识别图片中的文字及位置（用于表格识别）

        Args:
            image: 图片数据 (numpy array)
            language: 语言代码
            use_angle_cls: 是否使用方向分类

        Returns:
            list of dict with keys: text, x, y, confidence
        """
        self._init_ocr(language, use_angle_cls)
        result = self._ocr_instance.predict(image)

        if not result:
            return []

        # 提取文字和位置信息
        cells = []
        for res in result:
            # 检查是否是新的返回格式（对象属性）
            if hasattr(res, 'rec_texts') and hasattr(res, 'rec_boxes'):
                rec_texts = res.rec_texts
                rec_boxes = res.rec_boxes
                rec_scores = res.rec_scores if hasattr(res, 'rec_scores') else [1.0] * len(rec_texts)
                for text, box, score in zip(rec_texts, rec_boxes, rec_scores):
                    # box 格式: [x1, y1, x2, y2]
                    center_x = (box[0] + box[2]) / 2
                    center_y = (box[1] + box[3]) / 2
                    cells.append({
                        "text": str(text),
                        "x": center_x,
                        "y": center_y,
                        "confidence": float(score),
                    })
            # 兼容旧格式（字典）
            elif isinstance(res, dict) and 'rec_texts' in res and 'rec_boxes' in res:
                rec_texts = res['rec_texts']
                rec_boxes = res['rec_boxes']
                rec_scores = res.get('rec_scores', [1.0] * len(rec_texts))
                for text, box, score in zip(rec_texts, rec_boxes, rec_scores):
                    center_x = (box[0] + box[2]) / 2
                    center_y = (box[1] + box[3]) / 2
                    cells.append({
                        "text": str(text),
                        "x": center_x,
                        "y": center_y,
                        "confidence": float(score),
                    })

        return cells

    def clear_cache(self):
        """清除 OCR 实例缓存"""
        self._ocr_instance = None
        self._language = None
        self._use_angle_cls = None
