from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    return ReplyKeyboardMarkup([
        ["Start"],
        ["Указать адрес доставки", "Menu"]
    ])