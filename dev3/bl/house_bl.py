from dev3.sql import house_queries
from dev3.common import db
from sqlalchemy import text

class HouseBL:
    @staticmethod
    def create(society_id, wing, house_no, area_sq_ft, house_type, resident_name, resident_email, resident_phone):
        q = text(house_queries.insert_house())
        res = db.session.execute(q, {
            "society_id": society_id,
            "wing": wing,
            "house_no": house_no,
            "area_sq_ft": area_sq_ft,
            "house_type": house_type,
            "resident_name": resident_name,
            "resident_email": resident_email,
            "resident_phone": resident_phone
        })
        db.session.commit()
        return res.fetchone()

    @staticmethod
    def list_by_society(society_id):
        q = text(house_queries.list_houses_by_society())
        return db.session.execute(q, {"society_id": society_id}).fetchall()

    @staticmethod
    def get(house_id):
        q = text(house_queries.get_house_by_id())
        return db.session.execute(q, {"id": house_id}).fetchone()
