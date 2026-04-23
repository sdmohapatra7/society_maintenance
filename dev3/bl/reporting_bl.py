from dev3.sql import reporting_queries
from dev3.common import db
from sqlalchemy import text

class ReportingBL:
    @staticmethod
    def get_dashboard_stats():
        summary_q = text(reporting_queries.get_collection_summary())
        trends_q = text(reporting_queries.get_monthly_trends())
        
        summary = db.session.execute(summary_q).fetchall()
        trends = db.session.execute(trends_q).fetchall()
        
        return {
            "summary": [dict(row._mapping) for row in summary],
            "trends": [dict(row._mapping) for row in trends]
        }
