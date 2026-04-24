import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dev3.common import db
from dev3.__init__ import create_app
from sqlalchemy import text

app = create_app()
with app.app_context():
    sql = """
    CREATE TABLE IF NOT EXISTS user_setup_tokens (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        token VARCHAR(100) UNIQUE NOT NULL,
        expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        used BOOLEAN DEFAULT FALSE
    );
    """
    db.session.execute(text(sql))
    db.session.commit()
    print("user_setup_tokens table created.")
