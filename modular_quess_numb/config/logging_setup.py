import logging


def setup_logging():
    """
    Настройка логирования для всего проекта.
    - Консольный вывод
    - Единый формат
    """

    # 1. Формат сообщений
    formatter = logging.Formatter(
        '%(levelname)s | %(name)s | %(message)s'
    )

    # 2. Handler для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # для разработки
    console_handler.setFormatter(formatter)

    # 3. Root logger
    root_logger = logging.getLogger()        # глобальный логгер проекта
    root_logger.setLevel(logging.DEBUG)      # минимальный уровень логов

    # 4. Подключаем handler (только если ещё не добавлен)
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)