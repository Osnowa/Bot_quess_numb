from aiogram import Router
from aiogram.types import Message
from modular_quess_numb.config.users import get_game

router = Router()

@router.message()
async def process_other_answers(message: Message) -> None:
    game = get_game(message.from_user.id)
    if game.in_game:
        await message.answer('Мы сейчас играем. Отправляйте числа от 1 до 100')
    else:
        await message.answer('Я ограниченный бот. Давайте просто сыграем в игру?')
