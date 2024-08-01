from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
import logging
from datetime import datetime
from openai import OpenAI

router = Router()

SYSMSG = SystemMessage(content="Ты самый разговорчивый чат бот помощник из существующих, ты привые давать исчерпывающие ответы на вопросы пользователя и давать их абсолютно по делу. Твоя роль помогать сотрудникам офиса разобраться в проблемах в их сферах интересов, а также помогать с личными проблемами")
GPT_SYS_MSG = {"role": "system", "content": "Ты самый разговорчивый чат бот помощник из существующих, ты привые давать исчерпывающие ответы на вопросы пользователя и давать их абсолютно по делу. Твоя роль помогать сотрудникам офиса разобраться в проблемах в их сферах интересов, а также помогать с личными проблемами"}

IMAGEGEN_PROMPT = "Сгенерируй промпт для генерации картинки блюда по его описанию: "
RECEPT_PROMPT = "Сгенерируй рецепт блюда по описанию: "

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials='', verify_ssl_certs=False)


client = OpenAI(
    api_key="",
    base_url="https://api.proxyapi.ru/openai/v1",
)

user_messages = {}

'''
@router.message(F.text)
async def message_with_text(message: Message):
    chat_id = message.chat.id
    if user_exists(chat_id) == False:
        await message.answer('Вы не состоите в базе данных. Для общения добавьте себя в базу данных через кнопки и меню /start')    
    else:
        if chat_id not in user_messages.keys():
            user_messages[chat_id] = [SYSMSG]
        user_input = message.text
        add_chat_message(message.chat.id, user_input, datetime.now())
        user_messages[chat_id].append(HumanMessage(content=user_input))
        res = chat(user_messages[chat_id])
        user_messages[chat_id].append(res)
        await message.answer(res.content)
'''
    
@router.message(F.text)
async def message_gpt(message: Message):
    chat_id = message.chat.id
    if user_exists(chat_id) == False:
        await message.answer('Вы не состоите в базе данных. Для общения добавьте себя в базу данных через кнопки и меню /start')    
    else:
        if chat_id not in user_messages.keys():
            user_messages[chat_id] = [GPT_SYS_MSG]
        user_input = message.text
        add_chat_message(message.chat.id, user_input, datetime.now())
        user_messages[chat_id].append({"role": "user", "content": user_input})
        chat_completion = client.chat.completions.create(
                    model="gpt-3.5-turbo", 
                    messages=user_messages[chat_id]
        )
        res_text = chat_completion.choices[0].message.content
        user_messages[chat_id].append({"role": "assistant", "content": res_text})
        await message.answer(res_text)