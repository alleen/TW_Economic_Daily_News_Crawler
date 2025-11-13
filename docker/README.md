# Docker 部署指南

本文檔說明如何使用 Docker 容器化部署台灣經濟日報新聞爬蟲服務。

## 📋 前置需求

- Docker Engine 20.10 或更高版本
- Docker Compose 1.29 或更高版本

## 📁 檔案結構

```text
docker/
├── Dockerfile           # Docker 映像檔定義
├── .dockerignore       # 排除不必要的檔案
├── docker-compose.yml  # 容器編排配置
└── README_DOCKER.md    # 本文檔
```

## 🚀 快速開始

### 方法 1：使用 Docker Compose（推薦）

```bash
# 進入 docker 資料夾
cd docker

# 建立並啟動容器
docker-compose up -d

# 查看容器狀態
docker-compose ps

# 查看日誌
docker-compose logs -f

# 停止容器
docker-compose down
```

### 方法 2：使用 Docker 指令

```bash
# 建立 Docker image（從專案根目錄執行）
docker build -f docker/Dockerfile -t tw-economic-news-crawler .

# 執行容器
docker run -d \
  -p 127.0.0.1:3322:3322 \
  --name tw-news-crawler \
  --restart unless-stopped \
  tw-economic-news-crawler

# 查看容器日誌
docker logs -f tw-news-crawler

# 停止容器
docker stop tw-news-crawler

# 刪除容器
docker rm tw-news-crawler
```

## 🔗 訪問服務

容器啟動後，可透過以下網址訪問（僅限本機）：

- 主頁：<http://localhost:3322/>
- 財經新聞頁面：<http://localhost:3322/money>
- 國際新聞頁面：<http://localhost:3322/global>
- 財經新聞 API：<http://localhost:3322/money/scrape>
- 財經新聞 RSS：<http://localhost:3322/money/rss>
- 國際新聞 API：<http://localhost:3322/global/scrape>
- 國際新聞 RSS：<http://localhost:3322/global/rss>

## 🔒 安全性設定

### 本地存取限制

容器預設配置為**僅允許本機 (127.0.0.1) 存取**，這是透過 Docker port mapping 實現的：

```yaml
ports:
  - "127.0.0.1:3322:3322"  # 只綁定到本機 IP
```

這確保了外部網路無法直接訪問此服務，增加安全性。

### 開放外部存取（不推薦）

如果需要從其他機器訪問（例如開發環境），可以修改 `docker-compose.yml`：

```yaml
ports:
  - "3322:3322"  # 允許所有網路介面訪問
```

**⚠️ 警告**：開放外部存取前請確保已實施適當的安全措施。

## 🛠️ 常用操作

### 重新建立映像檔

```bash
cd docker
docker-compose build --no-cache
docker-compose up -d
```

### 更新容器

```bash
cd docker

# 停止並移除舊容器
docker-compose down

# 重新建立映像檔
docker-compose build

# 啟動新容器
docker-compose up -d
```

### 查看容器資源使用

```bash
docker stats tw-economic-news-crawler
```

### 進入容器內部

```bash
docker exec -it tw-economic-news-crawler /bin/bash
```

## 🐛 故障排除

### 容器無法啟動

```bash
# 查看詳細日誌
docker-compose logs

# 或使用 Docker 指令
docker logs tw-economic-news-crawler
```

### 端口已被佔用

如果 3322 端口已被使用，可以修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "127.0.0.1:8080:3322"  # 將主機端口改為 8080
```

### 重置容器

```bash
cd docker

# 完全清除容器、映像檔和網路
docker-compose down
docker rmi tw-economic-news-crawler
docker-compose up -d --build
```

## 📦 映像檔資訊

- **基礎映像**：`python:3.11-slim`
- **工作目錄**：`/app`
- **暴露端口**：`3322`
- **環境變數**：`PYTHONUNBUFFERED=1`

## 🔄 持續整合建議

### 自動化建置腳本

建立 `docker/build.sh`：

```bash
#!/bin/bash
cd "$(dirname "$0")"
docker-compose down
docker-compose build --no-cache
docker-compose up -d
echo "容器已成功啟動！"
docker-compose ps
```

### 定期更新

建議定期更新基礎映像以獲取安全性修補：

```bash
# 拉取最新的基礎映像
docker pull python:3.11-slim

# 重新建立映像檔
cd docker
docker-compose build --no-cache
docker-compose up -d
```

## 📝 環境變數

目前容器支援以下環境變數（可在 `docker-compose.yml` 中設定）：

- `PYTHONUNBUFFERED=1`：確保 Python 輸出不被緩衝，方便查看即時日誌

未來可擴展更多配置選項，例如：

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - LOG_LEVEL=INFO
  - PORT=3322
```

## 🤝 技術支援

如遇問題，請檢查：

1. Docker 和 Docker Compose 版本是否符合需求
2. 端口 3322 是否已被其他程式佔用
3. 容器日誌中是否有錯誤訊息
4. 網路連線是否正常（爬蟲需要訪問外部網站）

## 📄 授權

本專案遵循主專案的授權條款。
