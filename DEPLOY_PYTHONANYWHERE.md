# PythonAnywhereへのデプロイ手順

PythonAnywhereは、Pythonアプリケーションのホスティングに特化したプラットフォームで、無料プランでも利用できます。

## 手順

1. [PythonAnywhere](https://www.pythonanywhere.com/)でアカウントを作成

2. ダッシュボードから「Files」タブを選択し、アップロードボタンを使用してプロジェクトファイルをアップロード
   - ZIPファイルにまとめてアップロードすると便利です

3. 「Web」タブを選択し、「Add a new web app」をクリック

4. 「Manual configuration」を選択し、使用しているPythonバージョンを選択

5. 「Code」セクションで：
   - 「Source code」: アップロードしたプロジェクトのディレクトリパスを指定
   - 「Working directory」: 同じディレクトリパスを指定
   - 「WSGI configuration file」をクリックして編集

6. WSGI設定ファイルを以下のように編集：

```python
import sys
path = '/home/YourUsername/YourProjectDirectory'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

7. 「Virtualenv」セクションで新しい仮想環境を作成：
   - 「Enter path to a virtualenv」に仮想環境の名前を入力
   - 「Create」ボタンをクリック

8. 「Consoles」タブに移動し、「Start a new console」から「Bash」を選択

9. 以下のコマンドを実行して依存パッケージをインストール：
```bash
cd YourProjectDirectory
pip install -r requirements.txt
```

10. 「Web」タブに戻り、「Reload」ボタンをクリック

11. 表示されるURLからアプリにアクセス可能

## 注意事項

- OpenCVを使用する場合、PythonAnywhereでは追加の設定が必要な場合があります
- 無料プランでは外部からのリクエストに制限があります
- 画像処理などのCPU負荷の高い処理は、無料プランでは制限される可能性があります

## トラブルシューティング

- エラーが発生した場合は、「Web」タブの「Log files」セクションでエラーログを確認
- パッケージのインストールに問題がある場合は、PythonAnywhereのフォーラムで解決策を検索
