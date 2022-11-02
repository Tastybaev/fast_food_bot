from pymongo import MongoClient

from settings import MONGO_DB, MONGO_LINK


client = MongoClient(MONGO_LINK)
db = client[MONGO_DB]

def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({
        'user_id': effective_user.id,
    })
    if not user:
        user = {
            'user_id': effective_user.id,
            'first_name': effective_user.first_name,
            'last_name': effective_user.last_name,
            'username': effective_user.username,
            'chat_id': chat_id,
            # 'message_ids': []
        }
        db.users.insert_one(user)
    return user


def get_chat_id(db, effective_user):
    user = db.users.find_one({
        'user_id': effective_user.id,
    })
    return user['chat_id']


def create_message_id(db, effective_user, message_id):
    db.user.update_one(
        {'user_id': effective_user.id},
        {'$push':{'message_id': message_id}}
    )
    

def get_menu_drinks(db):
    menu_drinks = db.menu_drinks.find()
    return menu_drinks 


def get_menu_hot_dishes(db):
    menu_hot_dishes = db.menu_hot_dishes.find()
    return menu_hot_dishes


def get_menu_pizza(db):
    menu_pizza = db.menu_pizza.find()
    return menu_pizza


def get_menu_soup(db):
    menu_soup = db.menu_soup.find()
    return menu_soup
