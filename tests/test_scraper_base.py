# tests/test_base.py

import unittest
from unittest.mock import patch, MagicMock
import requests
from bs4 import BeautifulSoup

# テスト対象のBaseScraperクラスをインポート
from hp_items_scraping.scraper.base import BaseScraper


class TestBaseScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = BaseScraper()

    @patch("hp_items_scraping.scraper.base.time.sleep", return_value=None)
    def test_safe_request_success(self, patched_sleep):
        """
        safe_request()が正常に動作した場合のテスト
        ・ダミーのレスポンスを返すことを確認
        ・指定されたtimeoutが使用されることを確認
        """
        # ダミーのResponseオブジェクトを作成
        dummy_response = MagicMock(spec=requests.Response)
        dummy_response.status_code = 200
        dummy_response.text = (
            "<html><head><title>Test</title></head><body></body></html>"
        )
        dummy_response.raise_for_status.return_value = None

        # session.getをモック化して、dummy_responseを返すようにする
        with patch.object(
            self.scraper.session, "get", return_value=dummy_response
        ) as mock_get:
            response = self.scraper.safe_request("https://www.example.com")
            mock_get.assert_called_with(
                "https://www.example.com", timeout=self.scraper.timeout
            )
            self.assertEqual(response, dummy_response)

    @patch("hp_items_scraping.scraper.base.time.sleep", return_value=None)
    def test_safe_request_failure(self, patched_sleep):
        """
        safe_request()で例外が発生した場合のテスト
        ・例外が発生するとNoneを返すことを確認
        """
        with patch.object(
            self.scraper.session, "get", side_effect=requests.RequestException("Error")
        ) as mock_get:
            response = self.scraper.safe_request("https://www.example.com")
            mock_get.assert_called_with(
                "https://www.example.com", timeout=self.scraper.timeout
            )
            self.assertIsNone(response)

    @patch("hp_items_scraping.scraper.base.BaseScraper.safe_request")
    def test_get_soup_success(self, mock_safe_request):
        """
        get_soup()が正常にBeautifulSoupオブジェクトを返すかのテスト
        ・safe_request()からダミーのレスポンスを返し、HTMLタイトルが正しく抽出されることを確認
        """
        dummy_response = MagicMock(spec=requests.Response)
        dummy_response.text = (
            "<html><head><title>Test Title</title></head><body></body></html>"
        )
        mock_safe_request.return_value = dummy_response

        soup = self.scraper.get_soup("https://www.example.com")
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(soup.title.string, "Test Title")

    @patch("hp_items_scraping.scraper.base.BaseScraper.safe_request")
    def test_get_soup_failure(self, mock_safe_request):
        """
        get_soup()がsafe_request()からNoneを受け取った場合、Noneを返すことを確認
        """
        mock_safe_request.return_value = None
        soup = self.scraper.get_soup("https://www.example.com")
        self.assertIsNone(soup)


if __name__ == "__main__":
    unittest.main()
