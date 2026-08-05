# CloudOps

一個從容器化出發的 DevOps/SRE 學習專案，逐步把一支 Flask API 從本機部署到 AWS，並加上 CI/CD 與監控。

## 專案結構

```
cloudops/
├── app/                 # Flask API 應用程式
│   ├── app.py           # 主程式（/healthz + /todos CRUD）
│   ├── requirements.txt # 固定版本的依賴
│   ├── Dockerfile       # 多階段建置 + 非 root 執行
│   └── .dockerignore    # build context 忽略清單
├── nginx/
│   └── nginx.conf       # 反向代理：localhost:80 → app:5000
├── docker-compose.yml   # 容器編排（app + db + nginx）
├── .env.example         # 環境變數範本（複製成 .env 使用）
├── README.md            # 專案說明
└── .gitignore           # 忽略不需要版本控制的檔案
```

## 啟動（3 個服務）

```bash
# 1. 建立 .env（第一次才需要）
cp .env.example .env

# 2. 啟動服務（背景執行）
docker compose up -d

# 3. 查看容器狀態（三個都要 running）
docker compose ps

# 4. 健康檢查
curl http://localhost/healthz
# 預期回傳 {"status":"ok","database":"ok"}
```

## API 端點

| 方法 | 路徑 | 功能 |
|------|------|------|
| GET | `/healthz` | 健康檢查（含資料庫狀態） |
| GET | `/todos` | 列出所有待辦事項 |
| POST | `/todos` | 新增待辦（body: `{"title":"..."}`） |
| GET | `/todos/{id}` | 查詢單筆 |
| PATCH | `/todos/{id}` | 更新（body: `{"title":"...","done":true}`） |
| DELETE | `/todos/{id}` | 刪除 |

## 常用指令

```bash
docker compose ps        # 查看狀態
docker compose logs -f   # 查看即時日誌
docker compose down      # 停止（資料保留在 volume）
docker compose down -v   # 停止並刪除資料
```

## 架構

```
瀏覽器 ──► nginx(:80) ──► app(:5000) ──► postgres(:5432)
```
