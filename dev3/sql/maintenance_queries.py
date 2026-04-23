def insert_bill():
    return """
    INSERT INTO maintenance_bills (house_id, bill_month, amount, fixed_charge, area_charge, late_fee, other_charges, due_date, status)
    VALUES (:house_id, :bill_month, :amount, :fixed_charge, :area_charge, :late_fee, :other_charges, :due_date, :status)
    RETURNING id, house_id, amount;
    """

def get_bill_by_id():
    return """
    SELECT b.*, h.house_no, h.wing, s.name as society_name, s.address as society_address, h.resident_name, h.resident_email
    FROM maintenance_bills b
    JOIN houses h ON b.house_id = h.id
    JOIN societies s ON h.society_id = s.id
    WHERE b.id = :id;
    """

def list_bills_by_house():
    return "SELECT * FROM maintenance_bills WHERE house_id = :house_id ORDER BY bill_month DESC;"

def update_bill_status():
    return "UPDATE maintenance_bills SET status = :status, paid_date = :paid_date WHERE id = :id RETURNING id, status;"

def get_bills_to_notify():
    return """
    SELECT b.*, h.resident_name, h.resident_email 
    FROM maintenance_bills b
    JOIN houses h ON b.house_id = h.id
    WHERE b.due_date = :due_date AND b.status = 'unpaid';
    """
