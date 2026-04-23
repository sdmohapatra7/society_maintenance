from flask_login import UserMixin
from dev3.bl.user_dbh import UserDBH

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.role = user_data['role']
        self.house_id = user_data.get('house_id')

def load_user_callback(user_id):
    user_data = UserDBH.get_by_id(int(user_id))
    if user_data:
        return User(dict(user_data._mapping))
    return None
