import cv2
import numpy as np
from sklearn.cluster import KMeans
import logging

logger = logging.getLogger(__name__)

class ColorAnalyzer:
    def __init__(self):
        # パーソナルカラータイプの特徴を定義
        # 色相（H）: 0-180の範囲（OpenCVのHSV形式）
        # 彩度（S）: 0-255の範囲
        # 明度（V）: 0-255の範囲
        # パーソナルカラータイプの特徴を定義 - より明確な差異を持たせるために調整
        # 色相（H）: 0-180の範囲（OpenCVのHSV形式）
        # 彩度（S）: 0-255の範囲
        # 明度（V）: 0-255の範囲
        self.color_types = {
            'イエベ春': {
                'hue_ranges': [(16, 28)],  # 黄みの明るい肌色 - 範囲を広げて明確化
                'saturation': (40, 140),  # より控えめな彩度 - 範囲を調整
                'value': (210, 255),  # 非常に明るい - 下限を上げて特徴を強調
                'undertone': 'warm',
                'contrast': 'low'
            },
            'ブルベ夏': {
                'hue_ranges': [(0, 12), (168, 180)],  # ピンクよりの肌色 - 範囲を調整
                'saturation': (5, 90),  # 彩度を低めに設定
                'value': (170, 225),  # 明度範囲を調整
                'undertone': 'cool',
                'contrast': 'low'
            },
            'イエベ秋': {
                'hue_ranges': [(28, 45)],  # より黄みが強く深い肌色 - 範囲を広げて明確化
                'saturation': (60, 220),  # より高い彩度 - 下限を上げて特徴を強調
                'value': (110, 170),  # より暗め - 上限を下げて特徴を強調
                'undertone': 'warm',
                'contrast': 'high'
            },
            'ブルベ冬': {
                'hue_ranges': [(0, 8), (172, 180)],  # 青みよりの肌色 - 範囲を調整
                'saturation': (20, 130),  # 彩度範囲を調整
                'value': (120, 190),  # より暗め - 上限を下げて特徴を強調
                'undertone': 'cool',
                'contrast': 'high'
            }
        }

    def _calculate_hue_distance(self, hue, target_ranges):
        """色相と目標範囲との最小距離を計算"""
        # 色相環上での最短距離を計算
        def hue_distance(h1, h2):
            # 色相は0-180の範囲で循環する
            d = abs(h1 - h2)
            return min(d, 180 - d)
        
        min_distance = float('inf')
        for lower, upper in target_ranges:
            # 範囲内の場合は距離0
            if lower <= hue <= upper:
                return 1.0
            
            # 範囲外の場合は、両端との距離の小さい方を採用
            d1 = hue_distance(hue, lower)
            d2 = hue_distance(hue, upper)
            min_distance = min(min_distance, min(d1, d2))
        
        # 距離を0-1のスコアに変換 - より急峻な曲線で差を強調
        # 最大距離が40度とし、さらに累乗して差を強調
        normalized_distance = min_distance / 40.0
        return max(0, 1 - normalized_distance ** 1.5)

    def _is_in_range(self, value, ranges):
        """値が指定された範囲内にあるかチェック"""
        return any(lower <= value <= upper for lower, upper in ranges)

    def _calculate_color_score(self, color, type_features):
        """色の特徴とタイプの特徴の一致度を計算"""
        h, s, v = color

        # 色相のスコア（距離に基づく計算）
        hue_score = self._calculate_hue_distance(h, type_features['hue_ranges'])

        # 彩度のスコア（ガウス分布で重み付け）
        s_mid = sum(type_features['saturation']) / 2
        s_range = type_features['saturation'][1] - type_features['saturation'][0]
        s_score = np.exp(-((s - s_mid) / (s_range/2)) ** 2)

        # 明度のスコア（ガウス分布で重み付け）
        v_mid = sum(type_features['value']) / 2
        v_range = type_features['value'][1] - type_features['value'][0]
        v_score = np.exp(-((v - v_mid) / (v_range/2)) ** 2)

        # イエベ秋の場合、明度の低さをより重視
        if 'イエベ秋' in type_features.get('undertone', ''):
            v_weight = 0.4
            h_weight = 0.4
            s_weight = 0.2
        else:
            v_weight = 0.3
            h_weight = 0.4
            s_weight = 0.3

        # 総合スコア（重み付け）
        return h_weight * hue_score + s_weight * s_score + v_weight * v_score

    def _extract_skin_color(self, face_img):
        """顔画像から肌色を抽出"""
        # HSV色空間に変換
        hsv = cv2.cvtColor(face_img, cv2.COLOR_BGR2HSV)

        # 肌色の範囲でマスク作成
        lower_skin = np.array([0, 20, 70])
        upper_skin = np.array([30, 180, 255])
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # マスクを適用して肌色領域を抽出
        skin_region = cv2.bitwise_and(hsv, hsv, mask=mask)

        # 有効なピクセルのみを抽出
        valid_pixels = skin_region[mask > 0]

        if len(valid_pixels) == 0:
            return None

        # K-meansクラスタリングで代表色を抽出
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        kmeans.fit(valid_pixels)

        # クラスタサイズを計算
        labels = kmeans.labels_
        cluster_sizes = np.bincount(labels)

        # 最大クラスタの中心を返す
        largest_cluster = np.argmax(cluster_sizes)
        return kmeans.cluster_centers_[largest_cluster]

    def analyze(self, face_img):
        """顔画像からパーソナルカラータイプを判定"""
        # 肌色抽出
        skin_color = self._extract_skin_color(face_img)
        if skin_color is None:
            raise ValueError('肌色を検出できませんでした。適切な顔画像を使用してください。')

        # 各タイプのスコアを計算
        scores = {}
        details = {
            'detected_color': {
                'hue': float(skin_color[0]),
                'saturation': float(skin_color[1]),
                'value': float(skin_color[2])
            },
            'type_scores': {}
        }

        for type_name, features in self.color_types.items():
            # 個別のスコアを計算 - より明確な差を出すために計算方法を調整
            h, s, v = skin_color
            hue_score = self._calculate_hue_distance(h, features['hue_ranges'])
            
            # 彩度のスコア計算を調整 - より鋭いガウス分布を使用
            s_mid = sum(features['saturation']) / 2
            s_range = features['saturation'][1] - features['saturation'][0]
            # 指数の係数を1.2に増やして、範囲外の値のスコア低下を急激にする
            s_score = np.exp(-1.2 * ((s - s_mid) / (s_range/2)) ** 2)
            
            # 明度のスコア計算を調整 - より積極的な差を減らす
            v_mid = sum(features['value']) / 2
            v_range = features['value'][1] - features['value'][0]
            # 指数の係数を0.8に下げて、範囲外の値でもスコアが急激に低下しないようにする
            v_score = np.exp(-0.8 * ((v - v_mid) / (v_range/2)) ** 2)

            # 重み付けの計算 - 各タイプの特徴を強調するために調整
            if type_name == 'イエベ春':
                # イエベ春は明るく温かみのある色相が特徴
                h_weight = 0.50  # 色相の重みを増やす
                s_weight = 0.30
                v_weight = 0.20  # 明度の重みを下げる
            elif type_name == 'ブルベ夏':
                # ブルベ夏は柔らかく淡い色相が特徴
                h_weight = 0.45
                s_weight = 0.30  # 彩度の重みを上げる
                v_weight = 0.25  # 明度の重みを下げる
            elif type_name == 'イエベ秋':
                # イエベ秋は深みと黄みの色相が特徴
                h_weight = 0.50  # 色相の重みを増やす
                s_weight = 0.35  # 彩度の重みを上げる
                v_weight = 0.15  # 明度の重みを下げる
            else:  # ブルベ冬
                # ブルベ冬は青みがかった色相とコントラストが特徴
                h_weight = 0.55  # 色相を最も重要視
                s_weight = 0.30
                v_weight = 0.15  # 明度の重みを下げる

            # スコア計算を調整してより適切な差を生む
            # 各スコアの強調を調整
            hue_score_enhanced = hue_score ** 1.2  # 色相は強調したまま
            s_score_enhanced = s_score ** 1.1   # 彩度も同じ
            v_score_enhanced = v_score ** 0.9   # 明度は強調を弱める
            
            # 重み付け合計
            total_score = h_weight * hue_score_enhanced + s_weight * s_score_enhanced + v_weight * v_score_enhanced
            
            # スコアの差を適切に強調するために累乗を調整
            # 累乗の値を1.2から1.1に下げて、よりバランスの取れた差を生む
            total_score = total_score ** 1.1
            
            scores[type_name] = total_score

            # 詳細情報を保存
            details['type_scores'][type_name] = {
                'total_score': float(total_score),
                'hue_score': float(hue_score),
                'saturation_score': float(s_score),
                'value_score': float(v_score),
                'weights': {
                    'hue': float(h_weight),
                    'saturation': float(s_weight),
                    'value': float(v_weight)
                },
                'ranges': {
                    'hue': features['hue_ranges'],
                    'saturation': features['saturation'],
                    'value': features['value']
                }
            }

        # スコアが非常に低い場合のみデフォルト値を返す
        # 閾値を0.2に下げて、より多くの場合で実際の計算結果を使用する
        max_score = max(scores.values())
        if max_score < 0.2:
            logger.info('スコアが非常に低いためデフォルト値（ブルベ夏）を返します')
            return 'ブルベ夏', details

        # 最もスコアの高いタイプを返す
        return max(scores.items(), key=lambda x: x[1])[0], details
