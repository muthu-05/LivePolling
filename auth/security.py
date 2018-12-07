from werkzeug.security import generate_password_hash, check_password_hash
from models.user import UserModel
import common.settings

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    print (username + ' and -- ' + password)
    if user and check_password_hash(user.password, password):
       return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
