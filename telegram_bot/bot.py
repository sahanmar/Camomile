import requests

from default_config import TelegramBotCfg
from time import sleep

from typing import List, Optional


class Bot:
    def __init__(self, api_key: str, name: str):
        self.api_key: str = api_key
        self.name: str = name

    @staticmethod
    def load_from_config(config: TelegramBotCfg):
        return Bot(config.api_key, config.name)

    def post_message_to_channel(self, article: str, chat_id: str) -> None:
        url = f"https://api.telegram.org/bot{self.api_key}/sendMessage?chat_id={chat_id}&text={article}"
        requests.get(url)

    def post_many(self, articles: List[str], chat_id: str, take: Optional[int] = None) -> None:
        if take is None:
            take = len(articles)
        for article in articles[:take]:
            self.post_message_to_channel(article, chat_id)
