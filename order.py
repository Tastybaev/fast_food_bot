from db import db, get_menu
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext.conversationhandler import ConversationHandler
from utils import main_keyboard, order_keyboard


def order_start(update, context):
    update.message.reply_text(
        'Собираетесь оформить заказ?',
        reply_markup=order_keyboard()
    )
    return 'name'


def order_name(update, context):
    if update.message.text == 'Заказать':
        update.message.reply_text(
            'Впишите номер выбранного блюда',
            reply_markup=ReplyKeyboardMarkup([
                ['Отменить']
            ])
        )
        return 'count_of_portions'
    update.message.reply_text(
        'Вы отменили офрмление заказа',
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END


def order_portion(update, context):
    if update.message.text != 'Отменить':
        menu = get_menu(db)
        for i in menu:
            if update.message.text == i['id']:
                update.message.reply_text('Укажите количество порций')
                return 'adress'
        else:
            update.message.reply_text(
                'Неверный номер блюда.\nУкажите корректный номер блюда',
                reply_markup=order_keyboard()
            )
            return 'name'
    else:
        update.message.reply_text(
                'Вы отменили заказ',
                reply_markup=main_keyboard()
            )
        return ConversationHandler.END


def order_adress(update, context):
    if update.message.text != 'Отменить':
        coords = update.message.location
        update.message.reply_text(
            f'Ваши адрес {coords}?\nЕсли нет, впишите адрес доставки',
            reply_markup=ReplyKeyboardMarkup([['Да'], ['Отменить']])
        )
        return 'payment'
    else:
        update.message.reply_text(
                'Вы отменили заказ',
                reply_markup=main_keyboard()
            )
        return ConversationHandler.END


def order_payment(update, context):
    if update.message.text != 'Отменить':
        update.message.reply_text('Произведите оплату')
        return 'complete'
    else:
        update.message.reply_text(
                'Вы отменили заказ',
                reply_markup=main_keyboard()
            )
        return ConversationHandler.END


def order_complete(update, context):
    update.message.reply_text(
        'Заказ принят',
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END


def order_stop(update, context):
    update.message.reply_text(
        'Оформление заказ отменено',
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END
