from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_pagination import InlineKeyboardPaginator
from telegram.ext import CallbackQueryHandler, ConversationHandler
from db import db, get_menu_drinks, get_menu_hot_dishes, get_menu_pizza, get_menu_soup

from settings import(
    ADD_TO_SHOPPING_CART,
    FIRST,
    SECOND,
    HOT_DISHES,
    SOUP,
    PIZZA,
    DRINKS
)

from utils import KEYBOARD_MENU, KEYBOARD_NAVIGATION


def start(update, _):
    """Вызывается по команде `/start`."""
    # Получаем пользователя, который запустил команду `/start`
    user = update.message.from_user
    # logger.info("Пользователь %s начал разговор", user.first_name)
    # Создаем `InlineKeyboard`, где каждая кнопка имеет 
    # отображаемый текст и строку `callback_data`
    # Клавиатура - это список строк кнопок, где каждая строка, 
    # в свою очередь, является списком `[[...]]`
    reply_markup = InlineKeyboardMarkup(KEYBOARD_MENU)
    # Отправляем сообщение с текстом и добавленной клавиатурой `reply_markup`
    update.message.reply_text(
        text=f"Здравствуйте {user['first_name']}, что будете заказывать?", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас состояние `FIRST`
    return FIRST


def start_over(update, _):
    """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
    # Получаем `CallbackQuery` из обновления `update`
    query = update.callback_query
    # На запросы обратного вызова необходимо ответить, 
    # даже если уведомление для пользователя не требуется.
    # В противном случае у некоторых клиентов могут возникнуть проблемы.
    query.answer()
    reply_markup = InlineKeyboardMarkup(KEYBOARD_MENU)
   # Отредактируем сообщение, вызвавшее обратный вызов.
   # Это создает ощущение интерактивного меню.
    query.edit_message_text(
        text="Меню", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас находимся в состоянии `FIRST`
    return FIRST


def hot_dishes(update, _):
    """Показ нового выбора кнопок"""
    menu = get_menu_hot_dishes(db)
    query = update.callback_query
    query.answer()
    button = [[InlineKeyboardButton("Добавить в корзину", callback_data=str(ADD_TO_SHOPPING_CART))]]
    reply_markup = InlineKeyboardMarkup(button)
    #надо сделать 3 сообщения вместо  одного.
    # надо сделать автомотическое срабатывание navigation_menu()
    for item in menu:
        query.edit_message_text(
            text=f"{item}", reply_markup=reply_markup,
        )
    return SECOND


def soup(update, _):
    """Показ нового выбора кнопок"""
    menu = get_menu_soup(db)
    query = update.callback_query
    query.answer()
    reply_markup = InlineKeyboardMarkup(KEYBOARD_NAVIGATION)
    for item in menu:
        query.edit_message_text(
            text=f"{item}", reply_markup=reply_markup,
        )
    return FIRST


def pizza(update, _):
    """Показ выбора кнопок"""
    menu = get_menu_pizza(db)
    query = update.callback_query
    query.answer()
    reply_markup = InlineKeyboardMarkup(KEYBOARD_NAVIGATION)
    for item in menu:
        query.edit_message_text(
            text=f"{item}", reply_markup=reply_markup,
        )
    # Переход в состояние разговора `SECOND`
    return FIRST


def drinks(update, _):
    """Показ выбора кнопок"""
    menu = get_menu_drinks(db)
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Добавить в корзину", callback_data=str(ADD_TO_SHOPPING_CART))]
    ]
    reply_markup = InlineKeyboardMarkup(KEYBOARD_NAVIGATION)
    for item in menu:
        query.edit_message_text(
            text=f"{item}", reply_markup=reply_markup,
        )
    return FIRST

# def add_to_shopping_cart(update, _):
# def shopping_cart()


def navigation_menu(update, _):
    query = update.callback_query
    query.answer()
    reply_markup = InlineKeyboardMarkup(KEYBOARD_NAVIGATION)
    query.edit_message_text(
        text="Для оформления заказа выбирите блюда и перейдите в корзину",
        reply_markup=reply_markup
    )
    return SECOND


def end(update, _):
    """Возвращает `ConversationHandler.END`, который говорит 
    `ConversationHandler` что разговор окончен"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END
