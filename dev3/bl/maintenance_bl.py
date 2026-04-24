import os
from dev3.sql import maintenance_queries
from dev3.common import db
from sqlalchemy import text
from flask import current_app

class MaintenanceBL:
    @staticmethod
    def create_bill(house_id, bill_month, amount, fixed_charge, area_charge, due_date, status='unpaid'):
        from datetime import datetime
        
        # Ensure dates are in correct format
        if isinstance(bill_month, str):
            # Handle YYYY-MM or YYYY-MM-DD
            if len(bill_month) == 7: bill_month += "-01"
            bill_month = datetime.strptime(bill_month, '%Y-%m-%d').date()
            
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

        q = text(maintenance_queries.insert_bill())
        res = db.session.execute(q, {
            "house_id": house_id,
            "bill_month": bill_month,
            "amount": amount,
            "fixed_charge": fixed_charge,
            "area_charge": area_charge,
            "late_fee": 0,
            "other_charges": 0,
            "due_date": due_date,
            "status": status
        })
        db.session.commit()
        return res.fetchone()

    @staticmethod
    def generate_invoice_html(bill_id):
        return "<html><body>Invoice Details Dummy</body></html>"

    @staticmethod
    def get_upcoming_notifications(date):
        q = text(maintenance_queries.get_bills_to_notify())
        return db.session.execute(q, {"due_date": date}).fetchall()
