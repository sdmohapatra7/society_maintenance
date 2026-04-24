import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dev3.common import db
from dev3.__init__ import create_app
from sqlalchemy import text

app = create_app()
with app.app_context():
    # Seed Accountant role permissions
    defaults = [
        ('accountant', 'billing', True),
        ('accountant', 'expenses', True),
        ('accountant', 'reports', True)
    ]
    
    for role, feature, access in defaults:
        db.session.execute(text("""
            INSERT INTO role_permissions (role, feature_name, can_access)
            VALUES (:role, :feature, :access)
            ON CONFLICT (role, feature_name) DO UPDATE SET can_access = EXCLUDED.can_access
        """), {"role": role, "feature": feature, "access": access})
        
    db.session.commit()
    print("Accountant role permissions seeded.")
