from dev3.sql import complaint_queries
from dev3.common import db
from sqlalchemy import text

class ComplaintBL:
    @staticmethod
    def create(user_id: int, title: str, description: str, status: str | None = None):
        q = text(complaint_queries.insert_complaint())
        res = db.session.execute(q, {"user_id": user_id, "title": title, "description": description, "status": status})
        db.session.commit()
        return res.fetchone()

    @staticmethod
    def get(complaint_id: int):
        q = text(complaint_queries.get_complaint_by_id())
        return db.session.execute(q, {"id": complaint_id}).fetchone()

    @staticmethod
    def list_by_user(user_id: int):
        q = text(complaint_queries.list_complaints_by_user())
        return db.session.execute(q, {"user_id": user_id}).fetchall()

    @staticmethod
    def update_status(complaint_id: int, status: str):
        q = text(complaint_queries.update_complaint_status())
        res = db.session.execute(q, {"id": complaint_id, "status": status})
        db.session.commit()
        return res.fetchone()

    @staticmethod
    def delete(complaint_id: int):
        q = text(complaint_queries.delete_complaint())
        res = db.session.execute(q, {"id": complaint_id})
        db.session.commit()
        return res.fetchone()
