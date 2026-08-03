# CloudOps

## 專案結構

```
cloudops/
├── docker-compose.yml   # 容器編排設定
├── README.md            # 專案說明
└── .gitignore           # 忽略不需要版本控制的檔案
```

## 啟動 Nginx 服務

```bash
# 啟動服務（背景執行）
docker compose up -d

# 查看容器狀態
docker compose ps

# 停止服務
docker compose down

# 查看即時日誌
docker compose logs -f
```

啟動後開啟瀏覽器前往 `http://localhost` 即可看到 Nginx 預設頁面。將靜態檔案放入 `html/` 目錄即可自訂內容。
