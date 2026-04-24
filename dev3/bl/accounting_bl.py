from dev3.common import db
from sqlalchemy import text

class AccountingBL:
    @staticmethod
    def get_financial_summary():
        # Total Collected (Revenue)
        q_rev = text("SELECT SUM(amount) FROM maintenance_bills WHERE status = 'paid'")
        revenue = db.session.execute(q_rev).scalar() or 0
        
        # Total Expenses
        q_exp = text("SELECT SUM(amount) FROM expenses")
        expenses = db.session.execute(q_exp).scalar() or 0
        
        # Outstanding (Receivables)
        q_out = text("SELECT SUM(amount) FROM maintenance_bills WHERE status = 'unpaid'")
        outstanding = db.session.execute(q_out).scalar() or 0
        
        # Category-wise expenses
        q_cat = text("SELECT category, SUM(amount) as total FROM expenses GROUP BY category")
        cat_expenses = db.session.execute(q_cat).fetchall()
        
        return {
            "revenue": revenue,
            "expenses": expenses,
            "balance": revenue - expenses,
            "outstanding": outstanding,
            "cat_expenses": [dict(row._mapping) for row in cat_expenses]
        }
