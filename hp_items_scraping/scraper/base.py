"""
scraper/base.py

このモジュールは、共通のスクレイピングロジックを提供するBaseScraperクラスを定義します。
HTTPリクエストのセッション管理、エラーハンドリング、リクエスト間の遅延、HTMLのパースを担います。
"""

import time
import logging
import requests
from bs4 import BeautifulSoup
from hp_items_scraping import config  # config.pyから設定をインポート


class BaseScraper:
    def __init__(self):
        # requests.Session を用いて接続の再利用や共通ヘッダーの設定を行う
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)
        self.timeout = config.TIMEOUT
        self.request_delay = config.REQUEST_DELAY

    def safe_request(self, url):
        """
        指定されたURLに対してGETリクエストを行い、レスポンスを返します。
        エラー発生時はNoneを返し、ログにエラーメッセージを出力します。
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()  # ステータスコードが4xx,5xxの場合に例外を発生させる
            logging.info(f"Successfully fetched: {url}")
            # リクエスト間の待機時間を設定
            time.sleep(self.request_delay)
            return response
        except requests.RequestException as e:
            logging.error(f"Error during request to {url}: {e}")
            return None

    def get_soup(self, url):
        """
        指定されたURLのHTMLコンテンツをBeautifulSoupオブジェクトとして返します。
        リクエストに失敗した場合はNoneを返します。
        """
        response = self.safe_request(url)
        if response:
            response.encoding = "utf-8"
            return BeautifulSoup(response.text, "html.parser")
        else:
            logging.warning(f"Failed to get soup for URL: {url}")
            return None


# 例として、直接モジュールが実行された場合の簡単な動作確認
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    base_scraper = BaseScraper()
    test_url = "https://www.example.com"
    soup = base_scraper.get_soup(test_url)
    if soup:
        print(soup.title)
