import os
import tempfile
import unittest
from hp_items_scraping.utils import file_handler


class TestFileHandler(unittest.TestCase):

    def test_ensure_dir_creates_directory(self):
        # 一時ディレクトリ内で新たなディレクトリ作成のテスト
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = os.path.join(temp_dir, "nonexistent_dir")
            self.assertFalse(os.path.exists(new_dir))
            file_handler.ensure_dir(new_dir)
            self.assertTrue(os.path.exists(new_dir))
            self.assertTrue(os.path.isdir(new_dir))

    def test_write_and_read_csv(self):
        # 一時ディレクトリ内でCSVファイルの書き込みと読み込みのテスト
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file_path = os.path.join(temp_dir, "test.csv")
            header = ["id", "name", "value"]
            records = [[1, "Alice", 100], [2, "Bob", 200]]
            # CSV書き込み
            file_handler.write_csv(csv_file_path, header, records)
            # CSV読み込み
            read_data = file_handler.read_csv(csv_file_path)
            # CSVファイルは全て文字列として読み込まれるため、期待値も文字列に合わせる
            expected_data = [
                ["id", "name", "value"],
                ["1", "Alice", "100"],
                ["2", "Bob", "200"],
            ]
            self.assertEqual(read_data, expected_data)

    def test_read_csv_file_not_exist(self):
        # 存在しないファイルの読み込みで例外が発生するかのテスト
        with tempfile.TemporaryDirectory() as temp_dir:
            non_existent_file = os.path.join(temp_dir, "nofile.csv")
            self.assertFalse(os.path.exists(non_existent_file))
            with self.assertRaises(Exception):
                file_handler.read_csv(non_existent_file)


if __name__ == "__main__":
    unittest.main()
