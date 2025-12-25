import os
import time
import telebot
from telebot import types
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(BOT_TOKEN)
ADMIN_ID = None

@bot.message_handler(commands=['start'])
def start(message):
    global ADMIN_ID
    ADMIN_ID = message.from_user.id
    bot.send_message(message.chat.id, "Привет! Я буду присылать черновики для канала «АвтоКоротко | РФ» 🚗")

def send_draft():
    if not ADMIN_ID:
        return

    text = (
        "🚗 Камеры начали чаще штрафовать за телефон\n\n"
        "Коротко — держать телефон в руках стало дороже.\n\n"
        "Что это значит:\n"
        "• штраф прилетает автоматически\n"
        "• «я просто посмотрел» не работает\n\n"
        "Руки — на руль 📵"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Опубликовать", callback_data="publish"),
        types.InlineKeyboardButton("❌ Отклонить", callback_data="cancel")
    )

    bot.send_message(ADMIN_ID, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "publish":
        bot.send_message(CHANNEL_ID, call.message.text)
        bot.send_message(call.message.chat.id, "✅ Опубликовано")
    elif call.data == "cancel":
        bot.send_message(call.message.chat.id, "❌ Черновик отклонён")

def scheduler():
    time.sleep(20)
    while True:
        send_draft()
        time.sleep(28800)  # 3 раза в день

if __name__ == "__main__":
    threading.Thread(target=scheduler, daemon=True).start()
    bot.infinity_polling()
