# Personal Color Diagnosis App

パーソナルカラー診断アプリケーション - あなたに最適な色を見つけましょう！

## 機能

- リアルタイムのウェブカメラ診断
- 画像アップロードによる診断
- 4つのパーソナルカラータイプの判定
  - イエベ春
  - ブルベ夏
  - イエベ秋
  - ブルベ冬
- 詳細な診断結果と色の分析

## 技術スタック

- Backend: Python (Flask)
- Frontend: HTML, JavaScript
- 画像処理: OpenCV, NumPy
- 機械学習: scikit-learn (K-means clustering)

## セットアップ

1. リポジトリをクローン:
```bash
git clone [your-repo-url]
cd [your-repo-name]
```

2. 仮想環境を作成してアクティベート:
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
# または
.\venv\Scripts\activate  # Windows
```

3. 依存パッケージをインストール:
```bash
pip install -r requirements.txt
```

4. アプリケーションを起動:
```bash
python app.py
```

5. ブラウザで以下のURLにアクセス:
```
http://localhost:8080
```

## 使用方法

1. ウェブカメラを使用する場合は「カメラを使用」ボタンをクリック
2. または画像をアップロードして診断
3. 診断結果と推奨カラーのアドバイスを確認
4. 開発者ツール（F12）のコンソールで詳細な分析結果を確認可能

## デプロイ方法

### Renderへのデプロイ

1. [Render](https://render.com/)でアカウントを作成

2. GitHubリポジトリを連携：
   - Renderダッシュボードから「New +」→「Web Service」を選択
   - GitHubリポジトリを連携

3. 設定：
   - **Name**: personal-color-analyzer
   - **Environment**: Python
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn app:app`

4. 「Create Web Service」をクリック

5. デプロイが完了すると、アプリケーションのURLが提供されます

詳細な手順は[DEPLOY_RENDER.md](DEPLOY_RENDER.md)を参照してください。

## ライセンス

MIT License
