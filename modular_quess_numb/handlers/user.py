from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from modular_quess_numb.lexicon.lexicon import POSITIVE_ANSWERS, NEGATIVE_ANSWERS, LEXICON_RU
from modular_quess_numb.config.users import users, Game

router = Router()
DEFAULT_ATTEMPTS = 5 # попыток 5

def get_game(user_id: int) -> Game:
    """Получение объекта игры пользователя"""
    if user_id not in users:
        users[user_id] = Game(DEFAULT_ATTEMPTS)
    return users[user_id]

@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    user_id = message.from_user.id
    get_game(user_id)
    await message.answer(LEXICON_RU['/start'])

@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {DEFAULT_ATTEMPTS} попыток\n\n'
        f'Доступные команды:\n/help - правила и команды\n/cancel - выйти из игры\n'
        f'/stat - статистика\n\nДавай сыграем?'
    )

@router.message(Command(commands='stat'))
async def process_stat_command(message: Message) -> None:
    game = get_game(message.from_user.id)
    await message.answer(
        f'Всего игр сыграно: {game.total_games}\n'
        f'Игр выиграно: {game.wins}'
    )

@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message) -> None:
    game = get_game(message.from_user.id)
    if game.in_game:
        game.in_game = False
        await message.answer('Вы вышли из игры. Если захотите сыграть снова - напишите об этом')
    else:
        await message.answer('Мы и так не играем. Хотите начать игру?')

@router.message(F.text.lower().in_(POSITIVE_ANSWERS))
async def process_positive_answer(message: Message) -> None:
    game = get_game(message.from_user.id)
    if not game.in_game:
        users[message.from_user.id] = Game(DEFAULT_ATTEMPTS)
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, попробуй угадать!')
    else:
        await message.answer('Мы уже играем. Отправляйте числа от 1 до 100 или команды /cancel и /stat')

@router.message(F.text.lower().in_(NEGATIVE_ANSWERS))
async def process_negative_answer(message: Message) -> None:
    game = get_game(message.from_user.id)
    if not game.in_game:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом')
    else:
        await message.answer('Сейчас мы играем. Присылайте числа от 1 до 100')

@router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message) -> None:
    game = get_game(message.from_user.id)
    if not game.in_game:
        await message.answer('Мы еще не играем. Хотите сыграть?')
        return

    guess = int(message.text)
    result = game.check_guess(guess)

    if result == "win":
        await message.answer(f'Ура!!! Вы угадали число {guess}!\n\nХотите сыграть еще раз?')
    elif result == "lose":
        await message.answer(
            f'К сожалению, попытки закончились. Вы проиграли :(\n'
            f'Мое число было {game.secret_number}\n\nДавайте сыграем еще?'
        )
    elif result == "higher":
        await message.answer('Мое число больше')
    else:  # lower
        await message.answer('Мое число меньше')
