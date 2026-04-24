import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dev3.common import db
from dev3.__init__ import create_app
from sqlalchemy import text

app = create_app()
with app.app_context():
    # Create the role_permissions table
    sql = """
    CREATE TABLE IF NOT EXISTS role_permissions (
        id SERIAL PRIMARY KEY,
        role VARCHAR(50) NOT NULL,
        feature_name VARCHAR(100) NOT NULL,
        can_access BOOLEAN DEFAULT FALSE,
        UNIQUE(role, feature_name)
    );
    """
    db.session.execute(text(sql))
    
    # Seed default role permissions
    defaults = [
        ('admin', 'societies', True), ('admin', 'houses', True), ('admin', 'users', True), 
        ('admin', 'billing', True), ('admin', 'expenses', True), ('admin', 'complaints', True),
        ('resident', 'billing', True), ('resident', 'complaints', True),
        ('staff', 'complaints', True), ('staff', 'expenses', True)
    ]
    
    for role, feature, access in defaults:
        db.session.execute(text("""
            INSERT INTO role_permissions (role, feature_name, can_access)
            VALUES (:role, :feature, :access)
            ON CONFLICT (role, feature_name) DO UPDATE SET can_access = EXCLUDED.can_access
        """), {"role": role, "feature": feature, "access": access})
        
    db.session.commit()
    print("role_permissions table created and seeded successfully.")
