from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from db import (db, get_chat_id, get_menu, get_or_create_user)
from utils import (
    MENU,
    FIRST,
    KEYBOARD_MENU,
    KEYBOARD_SET_PORTION,
    SECOND,
    THIRD,
    edit_message_reply_markup,
    delete_message_all,
    save_message_id,
    send_message,
    create_menu_list,
    show_my_shopping_cart,
    delete_dish
)


def start(update, context):
    """Вызывается по команде `/start`."""
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    reply_markup = InlineKeyboardMarkup(KEYBOARD_MENU)
    message_id = update.message.reply_text(
        text=f"Здравствуйте {user['first_name']}, что будете заказывать?", reply_markup=reply_markup
    )
    context.user_data['message_ids'] = []
    save_message_id(context, message_id)
    return FIRST

def start_over(update, context):
    """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
    query = update.callback_query
    query.answer()
    chat_id = get_chat_id(db, update.effective_user)
    delete_message_all(context, chat_id)
    message_id = context.bot.send_message(
        chat_id=chat_id,
        text="Меню",
        reply_markup=InlineKeyboardMarkup(KEYBOARD_MENU)
    )
    save_message_id(context, message_id)
    return FIRST

def hot_dishes(update, context):
    """Показ нового выбора кнопок"""
    chat_id = get_chat_id(db, update.effective_user)
    menu_type = 'hot_dishes'
    menu = get_menu(menu_type)
    create_menu_list(context, menu_type)
    delete_message_all(context, chat_id)
    send_message(context, chat_id, menu, menu_type)
    return SECOND

def soup(update, context):
    """Показ нового выбора кнопок"""
    chat_id = get_chat_id(db, update.effective_user)
    menu_type = 'soup'
    menu = get_menu(menu_type)
    create_menu_list(context, menu_type)
    delete_message_all(context, chat_id)
    send_message(context, chat_id, menu, menu_type)
    return SECOND

def pizza(update, context):
    """Показ выбора кнопок"""
    chat_id = get_chat_id(db, update.effective_user)
    menu_type = 'pizza'
    menu = get_menu(menu_type)
    create_menu_list(context, menu_type)
    delete_message_all(context, chat_id)
    send_message(context, chat_id, menu, menu_type)
    return SECOND

def drinks(update, context):
    """Показ выбора кнопок"""
    chat_id = get_chat_id(db, update.effective_user)
    menu_type = 'drinks'
    menu = get_menu(menu_type)
    create_menu_list(context, menu_type)
    delete_message_all(context, chat_id)
    send_message(context, chat_id, menu, menu_type)
    return SECOND

def add_to_shopping_cart(update, context):
    query = update.callback_query
    query.answer()
    order = {}
    chat_id = get_chat_id(db, update.effective_user)
    message_id = query['message']['message_id']
    message = context.bot.edit_message_reply_markup(
        message_id=message_id,
        chat_id=chat_id,
        reply_markup=InlineKeyboardMarkup(KEYBOARD_SET_PORTION)
    )
    dish_type = message['caption'].split()[-1].split('.')[0]
    dish_id = message['caption'].split()[-1].split('.')[-1]
    order[dish_id] = 1

    if not context.user_data[dish_type]:
        context.user_data[dish_type].append(order)
    else:
        for dish in context.user_data[dish_type]:
            if dish.get(dish_id, False):
                dish[dish_id] += 1
                break
        else:
            context.user_data[dish_type].append(order)
    print(context.user_data)
    return SECOND


def delete_from_shopping_list(update, context):
    '''Удаление блюда из меню'''
    query = update.callback_query
    query.answer()
    message_id = query['message']['message_id']
    chat_id = get_chat_id(db, update.effective_user)
    flag = 'menu'
    delete_dish(context, chat_id, message_id, flag=flag)
    print(context.user_data)
    return SECOND


def increase_dish(update, context):
    query = update.callback_query
    query.answer()
    chat_id = get_chat_id(db, update.effective_user)
    message_id = query['message']['message_id']
    dish = query['message']['caption'].split()[-1]
    dish_id = dish.split('.')[-1]
    dish_type = dish.split('.')[0]
    for dish in context.user_data[dish_type]:
        if dish_id in dish:
            dish[dish_id] += 1
            dish_count = dish[dish_id]
            break
    edit_message_reply_markup(context, dish_count, message_id, chat_id)
    print(context.user_data)
    return SECOND


def decrease_dish(update, context):
    query = update.callback_query
    query.answer()
    chat_id = get_chat_id(db, update.effective_user)
    message_id = query['message']['message_id']
    dish = query['message']['caption'].split()[-1]
    dish_id = dish.split('.')[-1]
    dish_type = dish.split('.')[0]
    for dish in context.user_data[dish_type]:
        if dish_id in dish and dish[dish_id] > 0:
            dish[dish_id] -= 1
            dish_count = dish[dish_id]
            break
    edit_message_reply_markup(context, dish_count, message_id, chat_id)
    print(context.user_data)
    return SECOND


def my_shopping_cart(update, context):
    query = update.callback_query
    query.answer()
    chat_id = get_chat_id(db, update.effective_user)
    delete_message_all(context, chat_id)
    show_my_shopping_cart(context, chat_id)    
    return THIRD


def delete_from_shopping_cart(update, context):
    '''Удаление блюд из корзины '''
    query = update.callback_query
    query.answer()
    chat_id = get_chat_id(db, update.effective_user)
    message_id = query['message']['message_id']
    message = query['message']
    delete_dish(context, chat_id, message_id, message)
    return THIRD


def end(update, _):
    """Возвращает `ConversationHandler.END`, который говорит 
    `ConversationHandler` что разговор окончен"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END
