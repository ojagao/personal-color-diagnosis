from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os
from color_analyzer import ColorAnalyzer
from face_detector import FaceDetector
import logging

app = Flask(__name__)
CORS(app)

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

face_detector = FaceDetector()
color_analyzer = ColorAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'image' not in request.files:
            return jsonify({
                'error': '画像がアップロードされていません。'
            }), 400
        
        file = request.files['image']
        # 画像をバイトデータとして読み込み
        image_bytes = file.read()
        if not image_bytes:
            return jsonify({
                'error': '画像データが空です。'
            }), 400

        # 画像をデコード
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({
                'error': '画像の読み込みに失敗しました。別の画像を試してください。'
            }), 400

        # 画像サイズチェック
        if img.size == 0 or img.shape[0] == 0 or img.shape[1] == 0:
            return jsonify({
                'error': '無効な画像サイズです。'
            }), 400
        
        # 顔検出
        face = face_detector.detect_face(img)
        if face is None:
            return jsonify({
                'error': '顔を検出できませんでした。正面を向いて、明るい場所で撮影してください。'
            }), 400
        
        # パーソナルカラー分析
        try:
            color_type, details = color_analyzer.analyze(face)
            
            # 診断結果に応じたアドバイスを追加
            advice = {
                'イエベ春': 'クリアで明るい色がお似合いです。パステルカラーや明るいベージュがおすすめです。',
                'ブルベ夏': '柔らかく淡い色がお似合いです。グレイッシュなパステルカラーがおすすめです。',
                'イエベ秋': '深みのある落ち着いた色がお似合いです。アースカラーやテラコッタがおすすめです。',
                'ブルベ冬': 'クリアで鮮やかな色がお似合いです。ビビッドカラーやモノトーンがおすすめです。'
            }
            
            return jsonify({
                'result': color_type,
                'message': f'あなたは{color_type}タイプです。\n{advice[color_type]}',
                'details': details
            })
            
        except ValueError as e:
            return jsonify({
                'error': str(e)
            }), 400
            
    except Exception as e:
        logger.error(f'Error during analysis: {str(e)}')
        return jsonify({
            'error': '分析中にエラーが発生しました。もう一度お試しください。'
        }), 500

if __name__ == '__main__':
    # ローカル開発環境では固定ポートを使用
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', debug=False, port=port)
