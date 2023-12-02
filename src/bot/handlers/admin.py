import json
import os
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from src.bot.filters.admin import AdminFilter
from src.bot.structures.keyboards.reply_keyboards import admin_menu_mp
from src.configuration import conf
from src.db.database import Database

router = Router()


@router.message(Command(commands=["moderators"]), AdminFilter())
async def help_handler(
    message: Message,
    db: Database,
):
    moderators = await db.user.get_by_role()
    message_answer = ""
    for user in moderators:
        message_answer += f"{user.user_id}\n"
    await message.answer(message_answer)


@router.message(Command(commands=["admin"]), AdminFilter())
async def admin_menu_handler(message: Message):
    await message.answer("Меню Админа", reply_markup=admin_menu_mp)


@router.message(F.text == "Статистика")
async def stats_handler(message: Message, db: Database):
    await message.answer("Начал сбор статистики...")
    users = await db.user.get_all()
    await message.answer("Количество пользователей: " + str(len(users)))
    users_dict = [user.__dict__ for user in users]
    for item in users_dict:
        item.pop("_sa_instance_state", None)
        item.pop("waiting_for_continue", None)
        item.pop("id", None)
        for key, value in item.items():
            if isinstance(value, datetime):
                item[key] = value.strftime("%Y-%m-%d %H:%M:%S")

    with open(conf.paths.json_path, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=4)

    await message.answer_document(
        document=FSInputFile(conf.paths.json_path), caption="Сбор данных завершен"
    )
    os.remove(conf.paths.json_path)
