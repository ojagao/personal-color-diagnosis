# Google Cloud Runへのデプロイ手順

Google Cloud Runは、コンテナ化されたアプリケーションをサーバーレスで実行できるサービスです。スケーラビリティが高く、使用した分だけ課金されるため、効率的にアプリをホスティングできます。

## 前提条件

- Googleアカウントを持っていること
- Google Cloud Platformのプロジェクトを作成済みであること
- Google Cloud SDKがインストールされていること
- Dockerがインストールされていること

## 手順

### 1. Dockerfileの作成

プロジェクトのルートディレクトリに`Dockerfile`を作成します：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# OpenCVの依存関係をインストール
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 依存パッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# 環境変数を設定
ENV PORT 8080

# アプリケーションを実行
CMD exec gunicorn --bind :$PORT app:app
```

### 2. Google Cloudの設定

1. Google Cloud SDKを使用してログイン
```bash
gcloud auth login
```

2. プロジェクトを設定
```bash
gcloud config set project YOUR_PROJECT_ID
```

3. 必要なAPIを有効化
```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

### 3. アプリケーションのビルドとデプロイ

1. Dockerイメージをビルドしてコンテナレジストリにプッシュ
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/personal-color-analyzer
```

2. Cloud Runにデプロイ
```bash
gcloud run deploy personal-color-analyzer \
  --image gcr.io/YOUR_PROJECT_ID/personal-color-analyzer \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated
```

3. デプロイが完了すると、アプリケーションのURLが表示されます

## 注意事項

- Google Cloud Runは従量課金制ですが、無料枠があります
- メモリ使用量やCPU使用量に応じて課金されるため、リソース使用量を監視しましょう
- 画像処理などの重い処理を行う場合は、メモリ割り当てを増やす必要があるかもしれません：
```bash
gcloud run deploy personal-color-analyzer \
  --image gcr.io/YOUR_PROJECT_ID/personal-color-analyzer \
  --platform managed \
  --region asia-northeast1 \
  --memory 1Gi \
  --allow-unauthenticated
```

## トラブルシューティング

- デプロイに問題がある場合は、ログを確認：
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=personal-color-analyzer" --limit 50
```

- コンテナが起動しない場合は、Dockerfileを確認し、ローカルでテスト：
```bash
docker build -t personal-color-analyzer .
docker run -p 8080:8080 personal-color-analyzer
```
