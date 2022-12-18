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

def get_menu(menu_type):
    if menu_type == 'hot_dishes':
        return get_menu_hot_dishes(db)
    elif menu_type == 'soup':
        return get_menu_soup(db)
    elif menu_type == 'pizza':
        return get_menu_pizza(db)
    elif menu_type == 'drinks':
        return get_menu_drinks(db)  

def get_dish(dish_type, id):
    if dish_type == 'hot_dishes':
        return db.menu_hot_dishes.find_one({'id':id})
    elif dish_type == 'soup':
        return db.menu_soup.find_one({'id':id})
    elif dish_type == 'pizza':
        return db.menu_pizza.find_one({'id':id})
    elif dish_type == 'drinks':
        return db.menu_drinks.find_one({'id':id})
