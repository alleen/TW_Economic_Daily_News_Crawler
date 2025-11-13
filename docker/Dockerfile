# 使用官方 Python 運行時作為基礎映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 暴露應用程式運行的端口
EXPOSE 3322

# 設定環境變數
ENV PYTHONUNBUFFERED=1

# 運行應用程式
CMD ["python", "app.py"]
