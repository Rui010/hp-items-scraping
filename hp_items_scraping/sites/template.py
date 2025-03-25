# a_news.py

# サイト固有の定数（変更される可能性が低い場合はこのように直接埋め込みます）
NEWS_BASE_URL = "https://a-company.com/news/page/"
MAX_PAGE = 10
NEWS_DIR = "data/news"
CSV_FILENAME = "news.csv"

import logging
from urllib.parse import urljoin
from dataclasses import dataclass

from hp_items_scraping.scraper.base import BaseScraper
from hp_items_scraping.utils.file_handler import write_csv


@dataclass
class NewsItem:
    url: str
    date: str
    title: str
    content: str
    img_file_names: list

    def get_list(self):
        return [
            self.url,
            self.date,
            self.title,
            self.content,
            ",".join(self.img_file_names),
        ]


class ANewsScraper(BaseScraper):
    def __init__(self):
        super().__init__()

    def scrape_listing_page(self, page_number: int) -> list:
        url = urljoin(NEWS_BASE_URL, str(page_number))
        logging.info(f"Scraping listing page: {url}")
        soup = self.get_soup(url)
        if not soup:
            return []

        items = []
        # 仮のセレクタ例: ニュース一覧が <div class="news-list"> 内の <ul><li> にある前提
        news_list_items = soup.select("div.news-list > ul > li")
        for li in news_list_items:
            a_tag = li.find("a")
            if a_tag is None:
                continue
            article_url = a_tag.get("href")
            title = a_tag.text.strip()
            date_tag = li.find("span", class_="date")
            date_str = date_tag.text.strip() if date_tag else ""
            items.append({"url": article_url, "title": title, "date": date_str})
        return items

    def scrape_article_detail(self, article_url: str) -> dict:
        logging.info(f"Scraping article detail: {article_url}")
        soup = self.get_soup(article_url)
        if not soup:
            return {"content": "", "imgs": []}

        content_div = soup.select_one("div.article-content")
        content = content_div.text.strip() if content_div else ""
        img_elements = soup.select("div.article-content img")
        imgs = [img.get("src") for img in img_elements if img.get("src")]
        return {"content": content, "imgs": imgs}

    def scrape_all_news(self) -> list:
        news_items = []
        for page in range(1, MAX_PAGE + 1):
            listings = self.scrape_listing_page(page)
            for listing in listings:
                detail = self.scrape_article_detail(listing["url"])
                item = NewsItem(
                    url=listing["url"],
                    date=listing["date"],
                    title=listing["title"],
                    content=detail["content"],
                    img_file_names=detail["imgs"],
                )
                news_items.append(item)
        return news_items

    def save_news_csv(self, news_items: list):
        header = ["url", "date", "title", "content", "img_file_names"]
        csv_path = f"{NEWS_DIR}/{CSV_FILENAME}"
        records = [item.get_list() for item in news_items]
        write_csv(csv_path, header, records)
        logging.info(f"News CSV saved: {csv_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = ANewsScraper()
    news = scraper.scrape_all_news()
    scraper.save_news_csv(news)
