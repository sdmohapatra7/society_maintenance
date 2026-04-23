def insert_house():
    return """
    INSERT INTO houses (society_id, wing, house_no, area_sq_ft, house_type, resident_name, resident_email, resident_phone)
    VALUES (:society_id, :wing, :house_no, :area_sq_ft, :house_type, :resident_name, :resident_email, :resident_phone)
    RETURNING id, house_no, wing;
    """

def get_house_by_id():
    return "SELECT * FROM houses WHERE id = :id;"

def list_houses_by_society():
    return "SELECT * FROM houses WHERE society_id = :society_id ORDER BY wing, house_no;"

def update_house():
    return """
    UPDATE houses 
    SET wing = :wing, house_no = :house_no, area_sq_ft = :area_sq_ft, house_type = :house_type, 
        resident_name = :resident_name, resident_email = :resident_email, resident_phone = :resident_phone
    WHERE id = :id
    RETURNING id, house_no;
    """

def delete_house():
    return "DELETE FROM houses WHERE id = :id RETURNING id;"
