import json
import os
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from src.bot.filters.admin import AdminFilter
from src.bot.structures.keyboards.reply_keyboards import admin_menu_mp
from src.bot.structures.states.waiting_continue import AnnounceState
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

    await process_data(users_dict, conf.paths.text_path)

    await message.answer_document(
        document=FSInputFile(conf.paths.text_path), caption="Сбор данных завершен"
    )
    os.remove(conf.paths.json_path)
    os.remove(conf.paths.text_path)


@router.message(F.text == "Рассылка", AdminFilter())
async def announce_handler(message: Message, state: FSMContext):
    await state.set_state(AnnounceState.message)
    await message.answer("Отправьте текст рассылки")


@router.message(AnnounceState.message, AdminFilter())
async def announce_text_handler(message: Message, db: Database, state: FSMContext, bot: Bot):
    await state.clear()
    users = await db.user.get_users()
    await message.answer("Рассылка начата. Пользователей: " + str(len(users)))
    for user in users:
        await bot.send_message(chat_id=user.user_id, text=message.text)
    await message.answer("Рассылка завершена")


async def process_data(data, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        print(data)
        for item in data:
            try:
                user_id = item["user_id"]
                created_at = item["created_at"]
                first_name = item["first_name"]
                last_name = item["last_name"]
                user_name = item["user_name"]
                created_at_datetime = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                created_at_unix = created_at_datetime.timestamp()
                end_at = item.get("end_funnel_at")
                if end_at is not None:
                    end_at_datetime = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
                    end_at_unix = end_at_datetime.timestamp()
                    duration = (end_at_unix - created_at_unix) / 60
                stage = item["state"]
                output_file.write(f"Пользователь id: {user_id}, username: {user_name}, имя: {first_name}, фамилия: {last_name}\n")
                if end_at is not None:
                    output_file.write(f"Время прохождения: {duration:.2f} минут\n\n")
                else:
                    output_file.write(f"Сейчас на этапе: {stage}\n\n")
            except KeyError as e:
                output_file.write(f"Отсутствует ключ: {e}\n\n")
            except ValueError as e:
                output_file.write(f"Ошибка данных: {e}\n\n")


def calculate_duration(created_at, end_at):
    try:
        created_dt = datetime.fromisoformat(created_at)
        end_dt = datetime.fromisoformat(end_at)
    except ValueError:
        raise ValueError("Неверный формат времени")

    return (end_dt - created_dt).total_seconds() / 60
