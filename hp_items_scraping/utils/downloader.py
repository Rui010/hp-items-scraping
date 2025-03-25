"""
utils/downloader.py

このモジュールは、画像やPDFなどのファイルを指定されたURLからダウンロードし、
指定されたフォルダに保存する共通のダウンロード処理を提供します。
"""

import os
import logging
from urllib.parse import urlparse
import requests


def download_file(url: str, save_folder: str = "./") -> str:
    """
    指定したURLからファイルをダウンロードし、指定のフォルダに保存します。

    Args:
        url (str): ダウンロードするファイルのURL
        save_folder (str): ファイルの保存先フォルダ（デフォルトはカレントディレクトリ）

    Returns:
        str: 保存したファイルの名前。ダウンロードに失敗した場合は空文字列を返す。
    """
    try:
        # 保存先ディレクトリの存在チェックと作成
        if not os.path.exists(save_folder):
            os.makedirs(save_folder, exist_ok=True)
            logging.info(f"Directory created: {save_folder}")

        # URLからファイル名を抽出
        parsed_url = urlparse(url)
        file_name = os.path.basename(parsed_url.path)
        if not file_name:
            logging.error(f"ファイル名を抽出できませんでした。URL: {url}")
            return ""

        # ファイルのダウンロード
        response = requests.get(url)
        response.raise_for_status()  # エラー時に例外を発生させる
        file_path = os.path.join(save_folder, file_name)
        with open(file_path, "wb") as f:
            f.write(response.content)
        logging.info(f"ファイルをダウンロードしました: {file_path}")
        return file_name

    except requests.RequestException as req_err:
        logging.error(f"リクエストエラー: {req_err} - URL: {url}")
        return ""
    except Exception as e:
        logging.error(f"ダウンロード中にエラーが発生しました: {e} - URL: {url}")
        return ""


if __name__ == "__main__":
    # 簡単な動作確認用コード
    logging.basicConfig(level=logging.INFO)
    test_url = "https://www.example.com/sample.pdf"
    downloaded_file = download_file(test_url, "./downloads")
    print(f"Downloaded file: {downloaded_file}")
