from telegram_bot.bot import Bot
from default_config import DefaultConfig

cfg = DefaultConfig.load_default_config()
TelegramBot = Bot.load_from_config(cfg.telegram_bot)
