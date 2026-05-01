from dev3 import create_app
from dev3.bl.user_bl import UserBL

app = create_app()
with app.app_context():
    # Create an admin user
    success, res = UserBL.register("admin", "admin@society.com", "admin123", "admin")
    if success:
        print("Admin user created: admin / admin123")
    else:
        print(f"Failed to create admin: {res}")
    # Seed App Settings
    from dev3.common import db
    from sqlalchemy import text
    
    settings = [
        ('app_name', 'SocietyPro', 'The name of the application'),
        ('currency', '₹', 'Currency symbol used in the app'),
        ('admin_email', 'admin@society.com', 'System administrator email')
    ]
    for key, val, desc in settings:
        db.session.execute(text("""
            INSERT INTO app_settings (key, value, description) 
            VALUES (:key, :val, :desc) 
            ON CONFLICT (key) DO NOTHING
        """), {"key": key, "val": val, "desc": desc})
        
    # Seed Master Data
    master_data = [
        ('HOUSE_TYPE', '1BHK', '1BHK'),
        ('HOUSE_TYPE', '2BHK', '2BHK'),
        ('HOUSE_TYPE', '3BHK', '3BHK'),
        ('EXPENSE_CATEGORY', 'Maintenance', 'MAINTENANCE'),
        ('EXPENSE_CATEGORY', 'Electricity', 'ELECTRICITY'),
        ('EXPENSE_CATEGORY', 'Water', 'WATER'),
        ('EXPENSE_CATEGORY', 'Security', 'SECURITY')
    ]
    for cat, label, val in master_data:
        db.session.execute(text("""
            INSERT INTO master_data (category, label, value) 
            VALUES (:cat, :label, :val)
            ON CONFLICT DO NOTHING
        """), {"cat": cat, "label": label, "val": val})
        
    # Seed Roles
    roles = [
        ('admin', 'Full system access'),
        ('resident', 'Society resident access'),
        ('security_guard', 'Visitor and vehicle tracking'),
        ('accountant', 'Billing and expense management'),
        ('staff', 'General society management')
    ]
    for name, desc in roles:
        db.session.execute(text("""
            INSERT INTO roles (name, description) 
            VALUES (:name, :desc) 
            ON CONFLICT (name) DO NOTHING
        """), {"name": name, "desc": desc})

    # Seed Role Permissions (Basic defaults)
    features = ['dashboard', 'societies', 'users', 'billing', 'expenses', 'reports', 'complaints', 'events', 'visitors', 'vehicles', 'settings', 'access', 'accounting']
    for role_name, _ in roles:
        for feature in features:
            # Admins get everything, others get limited
            can_access = True if role_name == 'admin' else False
            
            # Custom defaults for roles
            if role_name == 'resident' and feature in ['dashboard', 'billing', 'complaints', 'events']:
                can_access = True
            if role_name == 'security_guard' and feature in ['dashboard', 'visitors', 'vehicles']:
                can_access = True
            if role_name == 'accountant' and feature in ['dashboard', 'billing', 'expenses', 'reports', 'accounting']:
                can_access = True
            if role_name == 'staff' and feature in ['dashboard', 'societies', 'users', 'billing', 'expenses', 'complaints', 'events', 'visitors', 'vehicles']:
                can_access = True
                
            db.session.execute(text("""
                INSERT INTO role_permissions (role, feature_name, can_access) 
                VALUES (:role, :feature, :access)
                ON CONFLICT (role, feature_name) DO NOTHING
            """), {"role": role_name, "feature": feature, "access": can_access})
        
    db.session.commit()
    print("Default settings, master data, roles, and permissions seeded.")

