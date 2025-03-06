# Renderへのデプロイ手順

Renderは比較的新しいホスティングプラットフォームで、無料枠があり、Herokuの代替として人気が高まっています。GitHubリポジトリと連携して簡単にデプロイできます。

## 前提条件

- Renderアカウントを作成済みであること
- GitHubアカウントを持っていること

## 手順

### 1. GitHubリポジトリの準備

1. GitHubにリポジトリを作成
2. プロジェクトをGitHubリポジトリにプッシュ：
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### 2. Renderでのデプロイ設定

1. [Render Dashboard](https://dashboard.render.com/)にログイン
2. 「New +」ボタンをクリックし、「Web Service」を選択
3. GitHubリポジトリを接続し、該当するリポジトリを選択
4. 以下の設定を行います：
   - **Name**: personal-color-analyzer（任意の名前）
   - **Environment**: Python
   - **Region**: 最寄りのリージョン（例：Singapore）
   - **Branch**: main（または使用しているブランチ）
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. 「Advanced」セクションを開き、環境変数を設定：
   - `PYTHON_VERSION`: 3.9.18

6. 「Create Web Service」ボタンをクリック

### 3. デプロイの確認

デプロイが完了すると、Renderはアプリケーションの公開URLを提供します。このURLからアプリにアクセスできます。

## 注意事項

- Renderの無料プランでは、一定時間使用がないとサービスがスリープ状態になります。最初のアクセス時に起動に時間がかかる場合があります。
- OpenCVを使用するアプリケーションでは、追加の設定が必要な場合があります。Renderのビルド環境で必要なパッケージをインストールするために、`build.sh`スクリプトを作成することをお勧めします。

### build.shの例

```bash
#!/usr/bin/env bash
# システム依存パッケージのインストール
apt-get update -y
apt-get install -y libgl1-mesa-glx libglib2.0-0

# Pythonパッケージのインストール
pip install -r requirements.txt
```

このスクリプトを作成し、Build Commandを`chmod +x build.sh && ./build.sh`に変更します。

## トラブルシューティング

- デプロイに問題がある場合は、Renderダッシュボードの「Logs」タブでログを確認できます。
- 特定のパッケージのインストールに問題がある場合は、`requirements.txt`のバージョン指定を確認してください。
- メモリ不足エラーが発生する場合は、有料プランへのアップグレードを検討してください。
