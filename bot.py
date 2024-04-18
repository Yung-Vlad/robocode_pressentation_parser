import json
import os
from typing import List

from aiogram import Bot, Dispatcher, types, enums
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from files import del_files
from http_operations import parse
from json_operations import check_data
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


async def run_bot() -> None:
    """Running bot"""

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def start_cmd(message: types.Message) -> None:
    """Handler for /start"""

    await message.answer("Привіт!😊😊😊\nЦей бот допоможе отримувати необхідні презентації по курсам.\n"
                         "Але для цього потрібно ввести пароль!")


@dp.message()
async def send_btn(message: types.Message) -> None:
    if message.text != "Robocode2024":
        return

    with open("logins.json", 'r') as file:
        data = json.load(file)

    buttons = [InlineKeyboardButton(text=course, callback_data=course) for course in data]
    buttons.append(InlineKeyboardButton(text="All courses", callback_data="All"))
    buttons_group = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons_group)

    await message.answer("Пароль вірний!😉\nВибери курс:", parse_mode=enums.parse_mode.ParseMode.MARKDOWN, reply_markup=keyboard)


@dp.callback_query()
async def send_presentation(callback: types.CallbackQuery) -> None:
    chat_id = callback.from_user.id
    data = callback.data

    if data == "All":
        await all_presentation(chat_id)
    elif check_data(data):  # Check course
        await process_presentation(chat_id, data)
    else:
        await error_msg(chat_id, data, "empty")


async def all_presentation(chat_id: int) -> None:
    with open("logins.json", 'r') as file:
        for course in json.load(file):
            if check_data(course):  # Check course
                await process_presentation(chat_id, course)
            else:
                await error_msg(chat_id, course, "empty")


async def process_presentation(chat_id: int, data: str) -> None:
    presentation = await parse(data)
    if not presentation:
        await error_msg(chat_id, data)
    else:
        await send_doc(presentation, chat_id)


async def error_msg(chat_id: int, course: str, key: str = "login_error") -> None:
    if key == "empty":
        await bot.send_message(chat_id, f"Немає інформації по даному курсу: {course}.")
    else:
        await bot.send_message(chat_id, f"Перевірте правильність даних від акаунту по даному курсу: {course}.")


async def send_doc(docs: List[str], chat_id: int) -> None:
    for doc_path in docs:
        file_name = os.path.basename(doc_path)

        pdf = FSInputFile(doc_path, filename=file_name)
        await bot.send_document(chat_id, pdf)
        del_files(doc_path)
