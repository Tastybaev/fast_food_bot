from curses import keyname
from settings import TELEGRAM_CHAT_ID
from db import db, get_or_create_user, get_menu
from utils import main_keyboard

def start_message(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    update.message.reply_text(
        f"Здравствуйте {user['first_name']}, что будете заказывать?",
        reply_markup = main_keyboard()
    )


def menu_message(update, context):
    menu = get_menu(db)
    update.message.reply_text(
        f"Мы предлагаем вам...\n{menu}",
        reply_markup = main_keyboard()
    )

# def answer(update, context):
#     chat = update.effective_chat
#     context.bot.send_message(chat_id = chat.id, text="Спасибо ваш заказ принят!")
