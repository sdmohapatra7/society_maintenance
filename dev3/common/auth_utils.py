from flask_login import UserMixin
from dev3.bl.user_dbh import UserDBH
from dev3.common import db
from sqlalchemy import text

class User(UserMixin):
    def __init__(self, user_data, permissions):
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.role = user_data['role']
        self.house_id = user_data.get('house_id')
        self.permissions = permissions
        
    def has_feature(self, feature_name):
        # Admin still has access to everything by default, but we'll check role_permissions too
        return feature_name in self.permissions

def load_user_callback(user_id):
    user_data = UserDBH.get_by_id(int(user_id))
    if user_data:
        # Fetch role-based permissions
        q = text("SELECT feature_name FROM role_permissions WHERE role = :role AND can_access = TRUE")
        perms_rows = db.session.execute(q, {"role": user_data.role}).fetchall()
        permissions = {r[0] for r in perms_rows}
        
        return User(dict(user_data._mapping), permissions)
    return None
