# tests/test_utils_downloader.py

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import requests

from hp_items_scraping.utils import downloader


class TestDownloader(unittest.TestCase):

    def setUp(self):
        # 一時ディレクトリを作成して、テスト後に自動で削除されるようにする
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    @patch("hp_items_scraping.utils.downloader.requests.get")
    def test_download_file_success(self, mock_get):
        """
        正常系テスト:
        - モックで成功したレスポンスを返し、指定されたフォルダにファイルが保存されることを検証する。
        """
        test_url = "https://www.example.com/sample.pdf"
        dummy_content = b"%PDF-1.4 sample content"
        dummy_response = MagicMock()
        dummy_response.content = dummy_content
        dummy_response.status_code = 200
        dummy_response.raise_for_status.return_value = None
        mock_get.return_value = dummy_response

        result = downloader.download_file(test_url, self.temp_dir.name)
        # URLから抽出されるファイル名は "sample.pdf" のはず
        self.assertEqual(result, "sample.pdf")

        # 保存先にファイルが作成され、内容が一致するかを検証
        file_path = os.path.join(self.temp_dir.name, "sample.pdf")
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "rb") as f:
            content = f.read()
        self.assertEqual(content, dummy_content)

    @patch("hp_items_scraping.utils.downloader.requests.get")
    def test_download_file_failure_request_exception(self, mock_get):
        """
        リクエスト時に例外が発生した場合、download_fileが空文字列を返すことを検証する。
        """
        test_url = "https://www.example.com/sample.pdf"
        mock_get.side_effect = requests.RequestException("Error")
        result = downloader.download_file(test_url, self.temp_dir.name)
        self.assertEqual(result, "")

    @patch("hp_items_scraping.utils.downloader.requests.get")
    def test_download_file_empty_filename(self, mock_get):
        """
        URLからファイル名が抽出できない場合、download_fileが空文字列を返すことを検証する。
        """
        test_url = "https://www.example.com/"  # ファイル名が存在しないURL
        dummy_response = MagicMock()
        dummy_response.content = b""
        dummy_response.status_code = 200
        dummy_response.raise_for_status.return_value = None
        mock_get.return_value = dummy_response

        result = downloader.download_file(test_url, self.temp_dir.name)
        self.assertEqual(result, "")

    @patch("hp_items_scraping.utils.downloader.requests.get")
    def test_download_file_other_exception(self, mock_get):
        """
        その他の例外（例: ファイル書き込み時の例外）が発生した場合、download_fileが空文字列を返すことを検証する。
        """
        test_url = "https://www.example.com/sample.pdf"
        dummy_content = b"dummy content"
        dummy_response = MagicMock()
        dummy_response.content = dummy_content
        dummy_response.status_code = 200
        dummy_response.raise_for_status.return_value = None
        mock_get.return_value = dummy_response

        # builtins.open をモック化して、ファイル書き込み時に例外を発生させる
        with patch("builtins.open", side_effect=Exception("Write error")):
            result = downloader.download_file(test_url, self.temp_dir.name)
            self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
