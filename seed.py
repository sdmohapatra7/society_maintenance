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
        
    db.session.commit()
    print("Default settings and master data seeded.")
