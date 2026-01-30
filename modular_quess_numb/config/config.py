from environs import Env
from dataclasses import dataclass

env = Env()
env.read_env()

@dataclass
class TgBot:
    token: str

def load_config() -> TgBot:
    """Загрузка конфигурации из переменных окружения"""
    return TgBot(token=env.str("BOT_TOKEN"))
