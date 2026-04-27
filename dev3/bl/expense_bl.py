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

    @staticmethod
    def update(expense_id: int, title: str, amount: float, category: str, expense_date, description: str, receipt_url: str):
        q = text("""
            UPDATE expenses 
            SET title = :title, amount = :amount, category = :category, 
                expense_date = :expense_date, description = :description, 
                receipt_url = COALESCE(:receipt_url, receipt_url)
            WHERE id = :id
        """)
        db.session.execute(q, {
            "id": expense_id,
            "title": title,
            "amount": amount,
            "category": category,
            "expense_date": expense_date,
            "description": description,
            "receipt_url": receipt_url
        })
        db.session.commit()
        return True

    @staticmethod
    def delete(expense_id: int):
        q = text("DELETE FROM expenses WHERE id = :id")
        db.session.execute(q, {"id": expense_id})
        db.session.commit()
        return True
