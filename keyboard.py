from telegram import InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from db import (
    db,
    get_menu_drinks,
    get_menu_hot_dishes,
    get_menu_pizza,
    get_menu_soup,
    get_or_create_user,
    get_chat_id
)

from settings import(
    FIRST,
    SECOND
)

from utils import (
    KEYBOARD_MENU,
    KEYBOARD_NAVIGATION,
    KEYBOARD_SHOPPING_CART,
    delete_message,
    send_message,
    save_message_id,
)


class Main():
    def start(self, update, context):
        """Вызывается по команде `/start`."""
        # Получаем пользователя, который запустил команду `/start`
        user = get_or_create_user(db, update.effective_user, update.message.chat_id)
        # logger.info("Пользователь %s начал разговор", user.first_name)
        # Создаем `InlineKeyboard`, где каждая кнопка имеет 
        # отображаемый текст и строку `callback_data`
        # Клавиатура - это список строк кнопок, где каждая строка, 
        # в свою очередь, является списком `[[...]]`
        reply_markup = InlineKeyboardMarkup(KEYBOARD_MENU)
        # Отправляем сообщение с текстом и добавленной клавиатурой `reply_markup`
        message_id = update.message.reply_text(
            text=f"Здравствуйте {user['first_name']}, что будете заказывать?", reply_markup=reply_markup
        )
        # Сообщаем `ConversationHandler`, что сейчас состояние `FIRST`
        context.user_data['message_ids'] = []
        save_message_id(message_id, context)
        return FIRST

    def start_over(self, update, context):
        """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
        # Получаем `CallbackQuery` из обновления `update`
        query = update.callback_query
        # На запросы обратного вызова необходимо ответить, 
        # даже если уведомление для пользователя не требуется.
        # В противном случае у некоторых клиентов могут возникнуть проблемы.
        query.answer()
        # Отредактируем сообщение, вызвавшее обратный вызов.
        # Это создает ощущение интерактивного меню.
        chat_id = get_chat_id(db, update.effective_user)
        delete_message(chat_id, context)
        message_id = context.bot.send_message(
            chat_id=chat_id,
            text="Меню",
            reply_markup=InlineKeyboardMarkup(KEYBOARD_MENU)
        )
        save_message_id(message_id, context)
        # Сообщаем `ConversationHandler`, что сейчас находимся в состоянии `FIRST`
        return FIRST

    def hot_dishes(self, update, context):
        """Показ нового выбора кнопок"""
        chat_id = get_chat_id(db, update.effective_user)
        menu = get_menu_hot_dishes(db)
        query = update.callback_query
        query.answer()
        delete_message(chat_id, context)
        send_message(menu, chat_id, context)
        return SECOND

    def soup(self, update, context):
        """Показ нового выбора кнопок"""
        chat_id = get_chat_id(db, update.effective_user)
        menu = get_menu_soup(db)
        query = update.callback_query
        query.answer()
        for item in menu:
            context.bot.send_message(
                chat_id=chat_id,
                text=f"{item}",
                reply_markup=InlineKeyboardMarkup(KEYBOARD_SHOPPING_CART),
            )
        context.bot.send_message(
            chat_id=chat_id,
            text="Для оформления заказа выбирите интересующее блюдо и перейдите в корзину.",
            reply_markup=InlineKeyboardMarkup(KEYBOARD_NAVIGATION)
        )
        return SECOND

    def pizza(self, update, context):
        """Показ выбора кнопок"""
        chat_id = get_chat_id(db, update.effective_user)
        menu = get_menu_pizza(db)
        query = update.callback_query
        query.answer()
        for item in menu:
            context.bot.send_message(
                chat_id=chat_id,
                text=f"{item}",
                reply_markup=InlineKeyboardMarkup(KEYBOARD_SHOPPING_CART),
            )
        context.bot.send_message(
            chat_id=chat_id,
            text="Для оформления заказа выбирите интересующее блюдо и перейдите в корзину.",
            reply_markup=InlineKeyboardMarkup(KEYBOARD_NAVIGATION)
        )
        return SECOND

    def drinks(self, update, context):
        """Показ выбора кнопок"""
        chat_id = get_chat_id(db, update.effective_user)
        menu = get_menu_drinks(db)
        query = update.callback_query
        query.answer()
        reply_markup = InlineKeyboardMarkup(KEYBOARD_SHOPPING_CART)
        for item in menu:
            context.bot.send_message(
                chat_id=chat_id,
                text=f"{item}",
                reply_markup=InlineKeyboardMarkup(KEYBOARD_SHOPPING_CART),
            )
        context.bot.send_message(
            chat_id=chat_id,
            text="Для оформления заказа выбирите интересующее блюдо и перейдите в корзину.",
            reply_markup=InlineKeyboardMarkup(KEYBOARD_NAVIGATION)
        )
        return SECOND

    def add_to_shopping_cart(self, update, _):
        query = update.callback_query
        query.answer()
        reply_markup = InlineKeyboardMarkup(KEYBOARD_NAVIGATION)
        _.user_data['hot_dishes'] = ['1']
        # Надо доделать добавление id в корзину.

    # def my_shopping_cart(update, _):

    def end(self, update, _):
        """Возвращает `ConversationHandler.END`, который говорит 
        `ConversationHandler` что разговор окончен"""
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="See you next time!")
        return ConversationHandler.END
