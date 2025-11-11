# 📰 台灣新聞爬蟲系統

## 📌 概述

一個能夠自動從多個台灣新聞網站抓取最新新聞的爬蟲工具，支援 RSS 2.0 格式輸出。利用 Flask 建立 API 後端，透過爬蟲程式取得即時新聞內容，並提供友善的網頁介面。

### 支援的新聞來源

- **經濟日報** (<https://money.udn.com/money/index>)
- **轉角國際** (<https://global.udn.com/global_vision/cate/120868>)

---

## 📌 功能特色

- ✅ 支援多個新聞來源，各自獨立的爬取介面
- ✅ 自動爬取新聞標題、發布時間、作者及完整內容
- ✅ 提供 RSS 2.0 格式訂閱功能
- ✅ 支援 JSON 格式 API 輸出
- ✅ 複製結果功能，方便快速取得資料
- ✅ 安全性：僅接受來自 127.0.0.1 的本地請求
- ✅ 響應式網頁設計，友善的使用者介面

---

## 📌 運作流程

1. **啟動 Flask 伺服器**：執行 `app.py` 啟動後端伺服器
2. **選擇新聞來源**：從首頁選擇要爬取的新聞來源（經濟日報或轉角國際）
3. **爬取新聞**：點擊「開始爬取新聞」按鈕
4. **執行爬蟲**：後端爬蟲程式抓取新聞內容並回傳 JSON 資料
5. **顯示結果**：結果以 JSON 格式顯示，可複製或清除

---

## 📌 環境設定及運行

### 1. **環境需求**

- Python 3.7 或以上版本
- 必要套件：Flask、Requests、BeautifulSoup4、flask-cors

### 2. **安裝套件**

```bash
pip install -r requirements.txt
```

### 3. **啟動伺服器**

```bash
python app.py
```

伺服器將在 `http://127.0.0.1:5000` 上啟動。

### 4. **使用說明**

1. 開啟瀏覽器，進入 `http://127.0.0.1:5000`
2. 選擇要爬取的新聞來源（經濟日報或轉角國際）
3. 點擊「開始爬取新聞」按鈕
4. 等待爬取完成，新聞內容將以 JSON 格式顯示
5. 可使用「複製」按鈕複製結果，或點擊「清除」按鈕清空內容

---

## 📌 專案結構

```text
TW_Economic_Daily_News_Crawler/
├── app.py                  # Flask 主程式，定義所有路由
├── money_crawler.py        # 經濟日報爬蟲模組
├── global_crawler.py       # 轉角國際爬蟲模組
├── requirements.txt        # Python 套件需求
├── README.md              # 專案說明文件
├── templates/             # 網頁模板
│   ├── index.html        # 首頁（選擇新聞來源）
│   ├── money.html        # 經濟日報爬蟲頁面
│   └── global.html       # 轉角國際爬蟲頁面
└── test/                  # 測試腳本
    ├── test_rss.py       # RSS 功能測試
    ├── test_endpoints.py # API 端點測試
    ├── check_rss.py      # RSS 輸出檢查
    └── debug_global_time.py # 轉角國際時間欄位除錯
```

---

## 📌 API 端點說明

### 網頁路由

| 路由 | 說明 |
|------|------|
| `GET /` | 首頁，顯示新聞來源選單 |
| `GET /money` | 經濟日報爬蟲頁面 |
| `GET /global` | 轉角國際爬蟲頁面 |

### 經濟日報 API

#### GET /money/scrape

- **說明**：爬取經濟日報最新新聞
- **回應格式**：application/json
- **範例回應**：

```json
[
    {
        "title": "台股站穩2萬點 法人看好後市",
        "publish_time": "2025-11-11 08:30",
        "reporter": "記者王小明／台北報導",
        "content": "台股昨日在金融股帶動下...",
        "url": "https://money.udn.com/money/story/..."
    }
]
```

#### GET /money/rss

- **說明**：以 RSS 2.0 格式輸出經濟日報新聞
- **回應格式**：application/rss+xml
- **用途**：可訂閱至 RSS 閱讀器

### 轉角國際 API

#### GET /global/scrape

- **說明**：爬取轉角國際最新新聞
- **回應格式**：application/json
- **範例回應**：

```json
[
    {
        "title": "全球視野：國際新聞標題範例",
        "publish_time": "2025-11-11",
        "reporter": "轉角編輯部",
        "content": "這是轉角國際新聞內容的範例...",
        "url": "https://global.udn.com/global_vision/story/8662/1234567"
    }
]
```

#### GET /global/rss

- **說明**：以 RSS 2.0 格式輸出轉角國際新聞
- **回應格式**：application/rss+xml
- **用途**：可訂閱至 RSS 閱讀器

---

## 📌 安全性設定

本專案包含以下安全性措施：

1. **IP 白名單**：僅接受來自 `127.0.0.1` 的請求
2. **本地監聽**：Flask 伺服器僅綁定至 `127.0.0.1:5000`
3. **請求過濾**：使用 `@app.before_request` 中間件檢查來源 IP

⚠️ **注意**：此工具僅供學術研究和個人學習使用，請遵守新聞網站的使用條款及 robots.txt 規範。

---

## 📌 開發與測試

### 執行測試

```bash
# 測試 RSS 生成功能
python test/test_rss.py

# 測試所有 API 端點
python test/test_endpoints.py

# 檢查 RSS 輸出
python test/check_rss.py

# 除錯轉角國際時間欄位
python test/debug_global_time.py
```

### 爬蟲技術細節

**經濟日報爬蟲** (`money_crawler.py`)：

- 目標頁面：<https://money.udn.com/money/index>
- 爬取策略：抓取所有 `/money/story/` 開頭的文章連結
- 時間格式：完整的日期時間字串

**轉角國際爬蟲** (`global_crawler.py`)：

- 目標頁面：<https://global.udn.com/global_vision/cate/120868>
- 爬取策略：抓取所有 `/global_vision/story/` 開頭的文章連結
- 時間格式：YYYY-MM-DD
- 特殊處理：移除 URL 中的 query string 參數

---

## 📌 常見問題

**Q: 為什麼爬取速度較慢？**
A: 為了避免對目標網站造成負擔，爬蟲會依序處理每篇文章。如有大量文章，需要較長時間。

**Q: 可以新增其他新聞來源嗎？**
A: 可以！參考 `money_crawler.py` 或 `global_crawler.py` 的結構，建立新的爬蟲模組，並在 `app.py` 中添加對應路由即可。

**Q: RSS 訂閱如何使用？**
A: 將 `http://127.0.0.1:5000/money/rss` 或 `http://127.0.0.1:5000/global/rss` 加入您的 RSS 閱讀器即可。

**Q: 為什麼只能本地訪問？**
A: 基於安全考量和網站使用條款，本工具僅供本地使用。如需遠端訪問，請自行評估法律風險。

---

## 📌 使用技術

- **後端框架**：Flask
- **爬蟲引擎**：BeautifulSoup4 + Requests
- **RSS 生成**：xml.etree.ElementTree
- **跨域支援**：flask-cors
- **前端**：原生 HTML/CSS/JavaScript

---

## 📌 版本資訊

### v2.0 (Current)

- ✨ 新增轉角國際新聞來源支援
- ✨ 重構首頁為選單式介面
- ✨ 新增 RSS 2.0 訂閱功能
- ✨ 分離 money 和 global 路由
- ✨ 新增安全性 IP 過濾
- ✨ 建立測試腳本目錄
- 🐛 修正轉角國際時間欄位爬取問題
- 🐛 修正 URL 路徑不一致問題

### v1.0

- 基本的經濟日報爬蟲功能
- 使用 Flask 提供 API 服務
- 簡單的網頁介面

---

## 📌 授權與免責聲明

本專案僅供教育和研究用途。使用者應：

1. 遵守目標網站的 robots.txt 和使用條款
2. 不得用於商業用途
3. 不得對目標網站造成過度負擔
4. 尊重原創內容的著作權

作者不對使用本工具造成的任何後果負責。

---

## 📌 貢獻

Fork 自 [https://github.com/davidhc1230/TW_Economic_Daily_News_Crawler](https://github.com/davidhc1230/TW_Economic_Daily_News_Crawler)

歡迎提交 Issue 或 Pull Request！

---

**原開發者**: [davidhc1230](https://github.com/davidhc1230)
**修改者**: [alleen](https://github.com/alleen)
**最後更新**: 2025-11-11
