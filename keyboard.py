from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from db import (db, get_chat_id, get_menu_drinks, get_menu_hot_dishes,
                get_menu_pizza, get_menu_soup, get_or_create_user)
from utils import (FIRST, KEYBOARD_MENU, KEYBOARD_SET_PORTION, SECOND,
                   delete_message, save_message_id, send_message)


def start(update, context):
    """Вызывается по команде `/start`."""
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    reply_markup = InlineKeyboardMarkup(KEYBOARD_MENU)
    message_id = update.message.reply_text(
        text=f"Здравствуйте {user['first_name']}, что будете заказывать?", reply_markup=reply_markup
    )
    context.user_data['message_ids'] = []
    save_message_id(message_id, context)
    return FIRST

def start_over(update, context):
    """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
    query = update.callback_query
    query.answer()
    chat_id = get_chat_id(db, update.effective_user)
    delete_message(chat_id, context)
    message_id = context.bot.send_message(
        chat_id=chat_id,
        text="Меню",
        reply_markup=InlineKeyboardMarkup(KEYBOARD_MENU)
    )
    save_message_id(message_id, context)
    return FIRST

def hot_dishes(update, context):
    """Показ нового выбора кнопок"""
    chat_id = get_chat_id(db, update.effective_user)
    menu = get_menu_hot_dishes(db)
    delete_message(chat_id, context)
    send_message(menu, chat_id, context)
    return SECOND

def soup(update, context):
    """Показ нового выбора кнопок"""
    chat_id = get_chat_id(db, update.effective_user)
    menu = get_menu_soup(db)
    delete_message(chat_id, context)
    send_message(menu, chat_id, context)
    return SECOND

def pizza(update, context):
    """Показ выбора кнопок"""
    chat_id = get_chat_id(db, update.effective_user)
    menu = get_menu_pizza(db)
    delete_message(chat_id, context)
    send_message(menu, chat_id, context)
    return SECOND

def drinks(update, context):
    """Показ выбора кнопок"""
    chat_id = get_chat_id(db, update.effective_user)
    menu = get_menu_drinks(db)
    delete_message(chat_id, context)
    send_message(menu, chat_id, context)
    return SECOND

def add_to_shopping_cart(update, context):
    query = update.callback_query
    query.answer()
    chat_id = get_chat_id(db, update.effective_user)
    message_id = query['message']['message_id']
    context.bot.edit_message_reply_markup(
        message_id=message_id,
        chat_id=chat_id,
        reply_markup=InlineKeyboardMarkup(KEYBOARD_SET_PORTION)
    )
    context.user_data['hot_dishes'] = ['1']
    return SECOND

# def my_shopping_cart(update, _):

def end(update, _):
    """Возвращает `ConversationHandler.END`, который говорит 
    `ConversationHandler` что разговор окончен"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END
