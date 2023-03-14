from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.dice import DiceEmoji

from chat_type import ChatTypeFilter

router = Router()
router.message.filter(
    ChatTypeFilter(chat_type = ["group", "supergroup", "private"]))

message_start="Бот находится в разработке. Бот умеет отвечает на соообщение сообщением, стикером на стикер, дальше планируется узнавать погоду, время, попытаться делать платежи."
message_help="Есть две команды start и help, можешь покидать мячик и кубик - dice and basketball"


@router.message(Command("start"))
async def cmd_dice_in_group(message: Message):
    await message.answer(message_start)
   

@router.message(Command("help"))
async def cmd_basketball_in_group(message: Message):
    await message.answer(message_help)

@router.message(Command("dice"))
async def cmd_dice_in_group(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)
   

@router.message(Command("basketball"))
async def cmd_basketball_in_group(message: Message):
    await message.answer_dice(emoji=DiceEmoji.BASKETBALL)
   