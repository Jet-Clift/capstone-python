from model import db, connect_to_db, User, Samps

def create_user(username, password):
    new_user = User(username=username, password=password)
    return new_user

