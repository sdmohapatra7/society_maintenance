def insert_user():
    return """
        INSERT INTO users (username, email, password, role, house_id)
        VALUES (:username, :email, :password, :role, :house_id)
        RETURNING id, username, email, role, house_id, is_active, created_at;
    """

def get_user_by_username():
    return """
        SELECT id, username, email, password, role, house_id, is_active FROM users WHERE username = :username;
    """

def get_user_by_id():
    return """
        SELECT id, username, email, password, role, house_id, is_active FROM users WHERE id = :id;
    """

def update_user_email():
    return """
        UPDATE users SET email = :email WHERE id = :id
        RETURNING id, username, email, is_active;
    """

def update_user_password():
    return """
        UPDATE users SET password = :password WHERE id = :id
        RETURNING id, username, email, is_active;
    """

def delete_user():
    return """
        DELETE FROM users WHERE id = :id RETURNING id;
    """
