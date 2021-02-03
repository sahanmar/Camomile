import json

from dataclasses import dataclass
from pathlib import Path

DEAFULT_PATH = Path("config.json")


@dataclass
class NewsCfg:
    name: str
    url: str
    news_type: str
    api_key: str


@dataclass
class TelegramBotCfg:
    name: str
    api_key: str


@dataclass
class TelegramChannelCfg:
    name: str
    chat_id: str


@dataclass
class DefaultConfig:
    news: NewsCfg
    telegram_bot: TelegramBotCfg
    telegram_chanel: TelegramChannelCfg

    @staticmethod
    def load_default_config(path: Path = DEAFULT_PATH):
        with open(path, "r") as f:
            config = json.load(f)
        return DefaultConfig(
            NewsCfg(**config["news"]),
            TelegramBotCfg(**config["telegram_bot"]),
            TelegramChannelCfg(**config["telegram_channel"]),
        )


print(DefaultConfig.load_default_config())
