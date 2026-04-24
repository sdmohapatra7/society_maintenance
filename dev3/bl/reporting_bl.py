from dev3.common import db
from sqlalchemy import text

class ReportingBL:
    @staticmethod
    def get_dashboard_stats():
        # 1. Society-wise Collection Summary
        summary_q = text("""
            SELECT s.name, 
                   COALESCE(SUM(CASE WHEN b.status = 'paid' THEN b.amount ELSE 0 END), 0) as total_collected,
                   COALESCE(SUM(CASE WHEN b.status = 'unpaid' THEN b.amount ELSE 0 END), 0) as total_pending,
                   COUNT(b.id) as total_bills
            FROM societies s
            LEFT JOIN houses h ON s.id = h.society_id
            LEFT JOIN maintenance_bills b ON h.id = b.house_id
            GROUP BY s.id, s.name
        """)
        
        # 2. Monthly Revenue Trends (Last 6 Months)
        revenue_trends_q = text("""
            SELECT TO_CHAR(bill_month, 'Mon YYYY') as month, 
                   COALESCE(SUM(amount), 0) as target, 
                   COALESCE(SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END), 0) as actual
            FROM maintenance_bills
            GROUP BY bill_month
            ORDER BY bill_month DESC
            LIMIT 6
        """)
        
        # 3. Expense vs Revenue Comparison
        # We'll join monthly revenue with monthly expenses
        comparison_q = text("""
            WITH rev AS (
                SELECT TO_CHAR(bill_month, 'Mon YYYY') as month, SUM(amount) as total FROM maintenance_bills WHERE status = 'paid' GROUP BY bill_month
            ),
            exp AS (
                SELECT TO_CHAR(expense_date, 'Mon YYYY') as month, SUM(amount) as total FROM expenses GROUP BY month
            )
            SELECT COALESCE(rev.month, exp.month) as month, 
                   COALESCE(rev.total, 0) as revenue, 
                   COALESCE(exp.total, 0) as expenses
            FROM rev
            FULL OUTER JOIN exp ON rev.month = exp.month
            ORDER BY month DESC LIMIT 6
        """)
        
        # 4. Complaint Status Distribution
        complaints_q = text("SELECT status, COUNT(*) as count FROM complaints GROUP BY status")
        
        summary = db.session.execute(summary_q).fetchall()
        revenue_trends = db.session.execute(revenue_trends_q).fetchall()
        comparison = db.session.execute(comparison_q).fetchall()
        complaints = db.session.execute(complaints_q).fetchall()
        
        return {
            "summary": [dict(row._mapping) for row in summary],
            "revenue_trends": [dict(row._mapping) for row in reversed(revenue_trends)],
            "comparison": [dict(row._mapping) for row in reversed(comparison)],
            "complaints": [dict(row._mapping) for row in complaints]
        }
