from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import llm


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Hello! I am not so smart google Flat5-base model, but i will answer you questions")


@router.message()
async def message_handler(msg: Message):
    #await msg.answer(f"Твой ID: {msg.from_user.id}")
    await msg.answer(llm.gen_reply(msg.text))