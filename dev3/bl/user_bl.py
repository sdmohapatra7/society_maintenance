from werkzeug.security import generate_password_hash, check_password_hash
from .user_dbh import UserDBH

class UserBL:
    @staticmethod
    def register(username: str, email: str, password: str, role: str = 'resident', house_id: int | None = None):
        # Check existing
        existing = UserDBH.get_by_username(username)
        if existing:
            return False, "Username already exists"
        pwd_hash = generate_password_hash(password)
        user = UserDBH.create_user(username, email, pwd_hash, role, house_id)
        return True, dict(user._mapping)

    @staticmethod
    def login(username: str, password: str):
        user = UserDBH.get_by_username(username)
        if not user:
            return False, "User not found"
        if not check_password_hash(user.password, password):
            return False, "Invalid credentials"
        if not user.is_active:
            return False, "User inactive"
        return True, dict(user._mapping)

    @staticmethod
    def update_email(user_id: int, email: str):
        user = UserDBH.update_email(user_id, email)
        return dict(user) if user else None

    @staticmethod
    def change_password(user_id: int, new_password: str):
        pwd_hash = generate_password_hash(new_password)
        user = UserDBH.update_password(user_id, pwd_hash)
        return dict(user) if user else None

    @staticmethod
    def delete(user_id: int):
        res = UserDBH.delete(user_id)
        return bool(res)
