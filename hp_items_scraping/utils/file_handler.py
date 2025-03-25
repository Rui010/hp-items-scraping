"""
utils/file_handler.py

このモジュールは、CSV出力、CSV読み込み、ディレクトリの存在確認と作成など、ファイル操作の共通処理を提供します。
"""

import csv
import os
import logging


def ensure_dir(directory: str):
    """
    指定したディレクトリが存在するか確認し、存在しない場合は作成します。

    Args:
        directory (str): チェックまたは作成するディレクトリのパス
    """
    try:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Directory ensured: {directory}")
    except Exception as e:
        logging.error(f"Error creating directory {directory}: {e}")
        raise


def write_csv(file_path: str, header: list, records: list):
    """
    指定されたパスにCSVファイルを書き出します。ファイルのディレクトリが存在しない場合は自動で作成します。

    Args:
        file_path (str): 書き出すCSVファイルのパス
        header (list): CSVのヘッダー（カラム名）のリスト
        records (list): 書き出すレコードのリスト。各レコードはリストで表現します。
    """
    # ファイルを保存するディレクトリが存在するか確認・作成
    dir_name = os.path.dirname(file_path)
    if dir_name:
        ensure_dir(dir_name)

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            for record in records:
                csv_writer.writerow(record)
        logging.info(f"CSV file written: {file_path}")
    except Exception as e:
        logging.error(f"Error writing CSV file {file_path}: {e}")
        raise


def read_csv(file_path: str) -> list:
    """
    指定されたCSVファイルを読み込み、内容を行ごとのリストとして返します。

    Args:
        file_path (str): 読み込むCSVファイルのパス

    Returns:
        list: CSVファイルの内容を表す行のリスト
    """
    records = []
    try:
        with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                records.append(row)
        logging.info(f"CSV file read: {file_path}")
    except Exception as e:
        logging.error(f"Error reading CSV file {file_path}: {e}")
        raise
    return records


# 直接実行された場合の簡単な動作確認用コード
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # テスト用のCSV書き込みと読み込みの例
    test_csv_path = "data/test/sample.csv"
    header = ["id", "name", "value"]
    records = [[1, "Alice", 100], [2, "Bob", 200]]

    write_csv(test_csv_path, header, records)
    read_data = read_csv(test_csv_path)
    print("Read CSV Data:")
    for row in read_data:
        print(row)
