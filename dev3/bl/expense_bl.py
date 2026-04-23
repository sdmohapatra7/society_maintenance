from dev3.sql import expense_queries
from dev3.common import db
from sqlalchemy import text

class ExpenseBL:
    @staticmethod
    def create(title: str, amount: float, category: str, expense_date, description: str, receipt_url: str):
        q = text(expense_queries.insert_expense())
        res = db.session.execute(q, {
            "title": title,
            "amount": amount,
            "category": category,
            "expense_date": expense_date,
            "description": description,
            "receipt_url": receipt_url
        })
        db.session.commit()
        return res.fetchone()

    @staticmethod
    def list_all():
        q = text(expense_queries.list_all_expenses())
        return db.session.execute(q).fetchall()
