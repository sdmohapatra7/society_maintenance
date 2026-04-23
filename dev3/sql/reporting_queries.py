def get_collection_summary():
    return """
    SELECT s.name, 
           SUM(CASE WHEN b.status = 'paid' THEN b.amount ELSE 0 END) as total_collected,
           SUM(CASE WHEN b.status = 'unpaid' THEN b.amount ELSE 0 END) as total_pending,
           COUNT(b.id) as total_bills
    FROM societies s
    LEFT JOIN houses h ON s.id = h.society_id
    LEFT JOIN maintenance_bills b ON h.id = b.house_id
    GROUP BY s.id, s.name;
    """

def get_monthly_trends():
    return """
    SELECT TO_CHAR(bill_month, 'Mon YYYY') as month, 
           SUM(amount) as target, 
           SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END) as actual
    FROM maintenance_bills
    GROUP BY bill_month
    ORDER BY bill_month;
    """
