def insert_society():
    return """
    INSERT INTO societies (name, address, registration_no, contact_email)
    VALUES (:name, :address, :registration_no, :contact_email)
    RETURNING id, name, created_at;
    """

def get_society_by_id():
    return "SELECT * FROM societies WHERE id = :id;"

def list_societies():
    return "SELECT * FROM societies ORDER BY created_at DESC;"

def update_society():
    return """
    UPDATE societies 
    SET name = :name, address = :address, registration_no = :registration_no, contact_email = :contact_email
    WHERE id = :id
    RETURNING id, name;
    """

def delete_society():
    return "DELETE FROM societies WHERE id = :id RETURNING id;"
