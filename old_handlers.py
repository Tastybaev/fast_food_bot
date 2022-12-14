from db import db, get_menu_hot_dishes, get_or_create_user
from utils import main_keyboard


def start_message(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    update.message.reply_text(
        f"Здравствуйте {user['first_name']}, что будете заказывать?",
        reply_markup = main_keyboard()
    )


def menu_message(update, context):
    menu = get_menu_hot_dishes(db)
    text_menu = ''
    for i in menu:
        text_menu += f"НОМЕР БЛЮДА: {i['id']}\nНазвание: {i['name']}\nЦена: {i['price']}\nОписание: {i['description']}\n\n\n"
    update.message.reply_text(      
        f"Мы предлагаем вам:\n{text_menu}\nДля заказа нажмите 'Заказать'",
        reply_markup = main_keyboard()
    )
    

# def answer(update, context):
#     chat = update.effective_chat
#     context.bot.send_message(chat_id = chat.id, text="Спасибо ваш заказ принят!")
