#!/usr/bin/env bash
# システム依存パッケージのインストール
apt-get update -y
apt-get install -y libgl1-mesa-glx libglib2.0-0

# Pythonパッケージのインストール
pip install -r requirements.txt
