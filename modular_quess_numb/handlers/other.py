from aiogram import Router
from aiogram.types import Message
import requests

router = Router()


@router.message(lambda x: x.text in ("илья", "ИЛЬЯ", "Илья")) # хендлер, отправляем фото котика )
async def kotik(message: Message):
    cat_response = requests.get(url="https://api.thecatapi.com/v1/images/search")
    if cat_response.status_code == 200:
        cat_link = cat_response.json()[0]['url']
        await message.answer(cat_link)
    else:
        await message.answer("Что-то пошло не так, котиков не будет ( ")


@router.message()
async def process_other_answers(message: Message) -> None:
    await message.answer("Эй, я принимаю только числа или команды,"
                         " но если введешь имя автора, то отправлю котика =) "
                         )
