import logging

from default_config import DefaultConfig
from articles_scraper.news_scraper import get_articles

from telegram_bot import TelegramBot


def main():
    cfg = DefaultConfig.load_default_config()

    news = get_articles(cfg.news)

    TelegramBot.post_many(news, cfg.telegram_chanel.chat_id, take=10)


if __name__ == "__main__":

    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

    main()
