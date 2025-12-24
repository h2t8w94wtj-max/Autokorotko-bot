import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

ADMIN_ID = None

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    global ADMIN_ID
    ADMIN_ID = msg.from_user.id
    await msg.answer("Привет! Я буду присылать черновики для канала «АвтоКоротко | РФ» 🚗")

async def send_draft():
    text = (
        "🚗 Камеры начали чаще штрафовать за телефон\n\n"
        "Коротко — держать телефон в руках стало дороже.\n\n"
        "Что это значит:\n"
        "• штраф прилетает автоматически\n"
        "• «я просто посмотрел» не работает\n\n"
        "Руки — на руль 📵"
    )

    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✅ Опубликовать", callback_data="publish"),
        InlineKeyboardButton("❌ Отклонить", callback_data="cancel")
    )

    await bot.send_message(ADMIN_ID, text, reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "publish")
async def publish(cb: types.CallbackQuery):
    await bot.send_message(CHANNEL_ID, cb.message.text)
    await cb.message.answer("✅ Опубликовано")
    await cb.answer()

@dp.callback_query_handler(lambda c: c.data == "cancel")
async def cancel(cb: types.CallbackQuery):
    await cb.message.answer("❌ Черновик отклонён")
    await cb.answer()

async def scheduler():
    await asyncio.sleep(20)
    while True:
        if ADMIN_ID:
            await send_draft()
        await asyncio.sleep(28800)  # 3 раза в день

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(dp)
