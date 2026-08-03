# ---------- Stage 1: builder（建造間）----------
# 用途：安裝 Python 依賴
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ---------- Stage 2: runtime（成品間）----------
# 用途：只保留執行所需的內容
FROM python:3.12-slim

WORKDIR /app

# 從 Stage 1 複製「已安裝的套件」（存在 /root/.local）
COPY --from=builder /root/.local /root/.local

# 讓系統找得到這些套件
ENV PATH=/root/.local/bin:$PATH

# 複製應用程式碼
COPY app.py .

# 非 root 使用者執行（資安最佳實踐）
USER nobody

EXPOSE 5000

# 健康檢查：用 Python 內建 urllib，避免額外安裝 curl
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/healthz', timeout=3)" || exit 1

CMD ["python", "app.py"]
