from dev3.sql import society_queries
from dev3.common import db
from sqlalchemy import text

class SocietyBL:
    @staticmethod
    def create(name, address, registration_no, contact_email):
        q = text(society_queries.insert_society())
        res = db.session.execute(q, {
            "name": name, 
            "address": address, 
            "registration_no": registration_no, 
            "contact_email": contact_email
        })
        db.session.commit()
        return res.fetchone()

    @staticmethod
    def get(society_id):
        q = text(society_queries.get_society_by_id())
        return db.session.execute(q, {"id": society_id}).fetchone()

    @staticmethod
    def list_all():
        q = text(society_queries.list_societies())
        return db.session.execute(q).fetchall()
