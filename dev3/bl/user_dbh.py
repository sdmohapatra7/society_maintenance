from dev3.common import db
from sqlalchemy import text
from dev3.sql import user_queries

class UserDBH:
    @staticmethod
    def create_user(username: str, email: str, password_hash: str, role: str = 'resident', house_id: int | None = None):
        q = text(user_queries.insert_user())
        res = db.session.execute(q, {
            "username": username, 
            "email": email, 
            "password": password_hash,
            "role": role,
            "house_id": house_id
        })
        db.session.commit()
        return res.fetchone()

    @staticmethod
    def get_by_username(username: str):
        q = text(user_queries.get_user_by_username())
        return db.session.execute(q, {"username": username}).fetchone()

    @staticmethod
    def get_by_id(user_id: int):
        q = text(user_queries.get_user_by_id())
        return db.session.execute(q, {"id": user_id}).fetchone()

    @staticmethod
    def update_email(user_id: int, email: str):
        q = text(user_queries.update_user_email())
        res = db.session.execute(q, {"id": user_id, "email": email})
        db.session.commit()
        return res.fetchone()

    @staticmethod
    def update_password(user_id: int, password_hash: str):
        q = text(user_queries.update_user_password())
        res = db.session.execute(q, {"id": user_id, "password": password_hash})
        db.session.commit()
        return res.fetchone()

    @staticmethod
    def delete(user_id: int):
        q = text(user_queries.delete_user())
        res = db.session.execute(q, {"id": user_id})
        db.session.commit()
        return res.fetchone()
