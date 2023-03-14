from aiogram import Router, F
from aiogram.types import Message
from chat_type import ContentTypeFilter
from function import randomize
import emoji


SET_STICK=('CAACAgIAAxkBAAEIBxhkBemsjuhfN_qLooxLEAekneexpAACaRUAAvjFmUqvL8mlrgukWC4E', 'CAACAgIAAxkBAAEIBxpkBepjz7dltoXLw-KGn0JR2oJT3gACxBIAAkOVmUpPyf4zUm0dLS4E','CAACAgIAAxkBAAEIBxxkBe7qd5O_9DfU5ykX72DjSkBAVQAC1xQAAtNFmUortHg5BFCMDi4E', 'CAACAgIAAxkBAAEIBx5kBe8DFaakOAn9pSdN-f7WQR7nfgAC4BQAAnRFmUpQYNm9rA82_i4E','CAACAgIAAxkBAAEIByBkBe81Fj1sRJM_VIU2QelJXPH7awACOiYAAq6GQEiIPfFQYVJF1y4E','CAACAgIAAxkBAAEIByJkBe9kSWKJJxqeTHQQhlaoY_ZIEgAClSsAAqd1OUkjHkw2LuCOHS4E')
SET_ANSWER = ('Ты осторожнее с такими выражениями, а то лимит умных фраз исчерпаешь.','Думаю, ты хотел зацепить меня, но не учел, что там, где ты учился, я преподавал.','Это не ты говоришь, а твои проекции.','Я вижу, что миллиарды лет эволюции прошли мимо тебя.')
RANDOM_ANWER_CHOISE = (True, False)

router = Router()
router.message.filter(
        ContentTypeFilter(type_message = ['text', 'animation','sticker', 'video', 'audio']))

@router.message(F.text)
async def message_with_text(message: Message):
    user_id = message.from_user.username
    if randomize(RANDOM_ANWER_CHOISE):
        await message.answer(f'{user_id} сказал, что он {message.text}.')
    else:
        await message.reply(emoji.emojize(":brain:"))

@router.message(F.sticker)
async def message_with_sticker(message: Message):
    random_stick = SET_STICK[randomize(SET_STICK)]
    randow_answer = SET_ANSWER[randomize(SET_ANSWER)]
    if randomize(RANDOM_ANWER_CHOISE):
        await message.answer(randow_answer)
    else:
        await message.answer_sticker(random_stick)

@router.message(F.animation)
async def message_with_animation(message: Message):
    await message.answer("Это анимация!")

@router.message(F.video)
async def message_with_animation(message: Message):
    await message.answer("Это видео!")

@router.message(F.audio)
async def message_with_animation(message: Message):
    await message.answer("Это аудио!")