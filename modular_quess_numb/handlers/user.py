from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from modular_quess_numb.lexicon.lexicon import POSITIVE_ANSWERS, NEGATIVE_ANSWERS, LEXICON_RU
import random
from modular_quess_numb.database.games import (
    get_active_game, finish_game, decrease_attempts, start_new_game, ATTEMPTS
)
from modular_quess_numb.database.users import (
    increment_total_games, increment_wins, get_user_by_telegram_id, create_user
)

router = Router()


@router.message(CommandStart()) # хендлер на команду старт
async def process_start_command(message: Message) -> None:
    telegram_id = message.from_user.id # получаем id пользователя
    user = get_user_by_telegram_id(telegram_id) # получаем из таблицы пользователя, если его нет, вернет False
    if not user:
        create_user(telegram_id) # создаем
    await message.answer(LEXICON_RU['/start'])

@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} попыток\n\n'
        f'Доступные команды:\n/help - правила и команды\n/cancel - выйти из игры\n'
        f'/stat - статистика\n\nДавай сыграем?'
    )

@router.message(Command(commands='stat'))
async def process_stat_command(message: Message) -> None:
    telegram_id = message.from_user.id
    user = get_user_by_telegram_id(telegram_id)

    await message.answer(
        f'Всего игр сыграно: {user[2]}\n'
        f'Игр выиграно: {user[3]}'
    )

@router.message(Command(commands='cancel')) # хендлер на обработку команды
async def process_cancel_command(message: Message) -> None:
    telegram_id = message.from_user.id
    user = get_user_by_telegram_id(telegram_id)
    game = get_active_game(user[0])
    if not game:
        await message.answer("Эй, мы еще не играем, что бы выходить =)")
    else:
        finish_game(game[0])
        await message.answer("Очень жаль что ты прервал игру, возвращайся ! ")


@router.message(F.text.lower().in_(POSITIVE_ANSWERS))
async def process_positive_answer(message: Message):
    telegram_id = message.from_user.id
    user = get_user_by_telegram_id(telegram_id)
    user_id = user[0]

    active_game = get_active_game(user_id)

    if not active_game:
        secret_number = random.randint(1, 100)
        start_new_game(user_id, secret_number)

        await message.answer(
            "Ура!\nЯ загадал число от 1 до 100. Попробуй угадать!"
        )
    else:
        await message.answer(
            "Мы уже играем. Присылай число от 1 до 100 🙂"
        )


@router.message(F.text.lower().in_(NEGATIVE_ANSWERS))
async def process_negative_answer(message: Message) -> None:
    await message.answer("Дружище, я принимаю только положительные числа от 1 до 100")

@router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    telegram_id = message.from_user.id
    user = get_user_by_telegram_id(telegram_id)
    user_id = user[0]

    game = get_active_game(user_id)

    if not game:
        await message.answer("Мы сейчас не играем. Хочешь начать?")
        return

    game_id, secret_number, attempts_left = game
    guess = int(message.text)

    if guess == secret_number:
        finish_game(game_id)
        increment_total_games(user_id)
        increment_wins(user_id)

        await message.answer(
            "🎉 Ты угадал число!\nХочешь сыграть ещё?"
        )
        return

    decrease_attempts(game_id)

    if attempts_left - 1 == 0:
        finish_game(game_id)
        increment_total_games(user_id)

        await message.answer(
            f"😢 Попытки закончились.\n"
            f"Я загадал число {secret_number}\n"
            f"Хочешь сыграть ещё?"
        )
        return

    if guess > secret_number:
        await message.answer("Моё число меньше")
    else:
        await message.answer("Моё число больше")
