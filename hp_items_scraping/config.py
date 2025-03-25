"""
config.py

このモジュールは、HP Items Scraping プロジェクトにおける各種設定・定数を定義します。
"""

# -----------------------
# リクエスト関連の設定
# -----------------------
TIMEOUT = 10  # HTTPリクエストのタイムアウト（秒）
REQUEST_DELAY = 2  # 各リクエスト間の待機時間（秒）
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/90.0.4430.93 Safari/537.36"
    )
}

# -----------------------
# ログ設定（必要に応じてlogging設定に利用）
# -----------------------
LOG_LEVEL = "INFO"

# -----------------------
# データ保存先ディレクトリおよびCSV出力設定
# -----------------------
DATA_DIR = "data"
