# パーソナルカラー分析アプリのデプロイ手順

## Herokuへのデプロイ方法

### 前提条件
- Herokuアカウントを作成済みであること
- Heroku CLIがインストールされていること
- Gitがインストールされていること

### デプロイ手順

1. Heroku CLIにログイン
```bash
heroku login
```

2. Gitリポジトリの初期化（まだ行っていない場合）
```bash
git init
git add .
git commit -m "Initial commit"
```

3. Herokuアプリの作成
```bash
heroku create your-app-name
```

4. Herokuにデプロイ
```bash
git push heroku main
```
または
```bash
git push heroku master
```

5. アプリを開く
```bash
heroku open
```

## 注意事項

- OpenCVの依存関係を解決するために、Herokuの「buildpacks」を追加する必要がある場合があります：
```bash
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt
```

- `Aptfile`を作成して以下の内容を追加：
```
libsm6
libxrender1
libfontconfig1
libice6
```

## トラブルシューティング

- デプロイに問題がある場合は、ログを確認：
```bash
heroku logs --tail
```

- メモリ不足エラーが発生する場合は、Herokuの有料プランへのアップグレードを検討してください。
