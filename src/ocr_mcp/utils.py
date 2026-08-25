"""
Utils - 工具函数
"""

import os
from pathlib import Path
from urllib.parse import urlparse


def is_url(source: str) -> bool:
    """判断是否为 URL"""
    parsed = urlparse(source)
    return parsed.scheme in ("http", "https")


def is_valid_image_path(path: str) -> bool:
    """判断是否为有效的图片路径"""
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}
    path = Path(path)
    return path.is_file() and path.suffix.lower() in valid_extensions


def get_image_info(image_path: str) -> dict:
    """获取图片基本信息"""
    import cv2

    image = cv2.imread(image_path)
    if image is None:
        return {"error": "无法读取图片"}

    height, width = image.shape[:2]
    channels = image.shape[2] if len(image.shape) > 2 else 1

    return {
        "width": width,
        "height": height,
        "channels": channels,
        "size_bytes": os.path.getsize(image_path),
    }
