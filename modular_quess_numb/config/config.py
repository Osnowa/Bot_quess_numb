from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


def load_config():
    env = Env()
    env.read_env()
    setting = TgBot(token=env("BOT_TOKEN"))
    return setting
