from db import db
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext.conversationhandler import ConversationHandler
from utils import main_keyboard


def order_start(update, context):
    update.message.reply_text(
        "Впишите название выбранного блюда",
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"


def order_name(update, context):
    order_name = update.message.text
    return 'name'


def order_stop(update, context):
    update.message.reply_text('Введите название блюда')