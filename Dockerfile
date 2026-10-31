FROM python:3.10-slim

# OpenCV / PaddlePaddle 运行所需系统库
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 libglib2.0-0 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir .

# stdio MCP server；OCR 引擎懒加载，启动无需下载模型
ENTRYPOINT ["python", "-m", "ocr_mcp"]
