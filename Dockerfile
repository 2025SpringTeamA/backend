FROM python:3.11-slim

WORKDIR /app

# pipをインストールするために必要なパッケージを追加
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# requirements.txtのコピーとインストール
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
ENV PYTHONPATH=/app

EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
