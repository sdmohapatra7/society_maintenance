from dev3 import create_app
from dev3.common import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    permissions = [
        # Staff
        ('staff', 'complaints', True),
        ('staff', 'visitors', True),
        ('staff', 'expenses', True),
        
        # Accountant
        ('accountant', 'accounting', True),
        ('accountant', 'billing', True),
        ('accountant', 'expenses', True),
        
        # Resident
        ('resident', 'billing', True),
        ('resident', 'complaints', True),
        ('resident', 'visitors', True),
        ('resident', 'vehicles', True),
        
        # Security Guard
        ('security_guard', 'visitors', True),
        ('security_guard', 'vehicles', True)
    ]
    
    for role, feature, access in permissions:
        db.session.execute(text("""
            INSERT INTO role_permissions (role, feature_name, can_access)
            VALUES (:role, :feature, :access)
            ON CONFLICT (role, feature_name) DO UPDATE SET can_access = EXCLUDED.can_access
        """), {"role": role, "feature": feature, "access": access})
        
    db.session.commit()
    print("Permissions re-seeded successfully.")
