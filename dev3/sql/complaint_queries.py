def insert_complaint():
    return """
        INSERT INTO complaints (user_id, title, description, status)
        VALUES (:user_id, :title, :description, COALESCE(:status, 'open'))
        RETURNING id, user_id, title, description, status, created_at;
    """

def get_complaint_by_id():
    return """
        SELECT id, user_id, title, description, status FROM complaints WHERE id = :id;
    """

def list_complaints_by_user():
    return """
        SELECT id, user_id, title, description, status FROM complaints WHERE user_id = :user_id ORDER BY created_at DESC;
    """

def update_complaint_status():
    return """
        UPDATE complaints SET status = :status WHERE id = :id
        RETURNING id, user_id, title, description, status;
    """

def delete_complaint():
    return """
        DELETE FROM complaints WHERE id = :id RETURNING id;
    """
