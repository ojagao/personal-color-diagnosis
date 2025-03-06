import cv2
import numpy as np

class FaceDetector:
    def __init__(self):
        # 事前学習済みの顔検出モデルを読み込み
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def detect_face(self, image):
        """画像から顔を検出し、顔の部分を切り出して返す"""
        # グレースケールに変換
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 顔検出
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return None
        
        # 最も大きい顔を選択
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        
        # 顔の部分を切り出し
        face_img = image[y:y+h, x:x+w]
        
        return face_img
