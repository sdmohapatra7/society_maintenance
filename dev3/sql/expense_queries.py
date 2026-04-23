def insert_expense():
    return """
        INSERT INTO expenses (title, amount, category, expense_date, description, receipt_url)
        VALUES (:title, :amount, :category, :expense_date, :description, :receipt_url)
        RETURNING id, title, amount, category, expense_date, description, receipt_url;
    """

def list_all_expenses():
    return """
        SELECT id, title, amount, category, expense_date, description, receipt_url FROM expenses ORDER BY expense_date DESC;
    """

def get_expense_by_id():
    return """
        SELECT id, title, amount, category, expense_date, description, receipt_url FROM expenses WHERE id = :id;
    """
