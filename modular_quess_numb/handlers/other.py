from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def process_other_answers(message: Message) -> None:
    pass
