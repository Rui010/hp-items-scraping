# HP Items Scraping

Web 制作の現場で、コーポレートサイトのリニューアルに伴う旧サイト情報の移行用データを自動で収集するためのスクレイピングツールです。

## 概要

本プロジェクトは、Python を用いて複数の企業サイトからニュースや商品情報、アワード情報などを収集し、CSV 形式などで出力するツールです。

- 共通処理（HTTP リクエスト、HTML パース、エラーハンドリング）は `hp_items_scraping/scraper/base.py` に実装
- サイト固有のスクレイピングロジックは `hp_items_scraping/sites/` 内に格納（例: `a_news.py`, `b_products.py` など）
- 画像や PDF などのファイルは、 `hp_items_scraping/utils/downloader.py` を利用してダウンロード
- 出力データは CSV 形式で、文字コードは BOM 付き UTF-8（`utf-8`）で保存

## 特徴

- **共通ライブラリ:**  
  `BaseScraper` により、HTTP リクエストや BeautifulSoup を使ったパース処理を共通化
- **サイト固有の処理:**  
  各サイトに合わせたスクレイピングロジックを個別のモジュールに実装
- **画像ダウンロード:**  
  画像の URL から実際に画像ファイルをダウンロードし、出力データにファイル名を記録
- **CSV 出力:**  
  日時付きのファイル名で CSV を出力し、データの整理・移行をサポート

# 設計ドキュメント

- **docs/design.md**: ディレクトリ構成とファイルの機能について記載

# 実行コマンド

## テスト実行方法

```
python -m unittest discover -s tests
```

## モジュールとして実行

```
python -m hp_items_scraping.scraper.base
python -m hp_items_scraping.sites.[ファイル名]

```
