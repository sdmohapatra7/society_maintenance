import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dev3.common import db
from dev3.__init__ import create_app
from sqlalchemy import text

app = create_app()
with app.app_context():
    # 1. App Settings Table
    db.session.execute(text("""
    CREATE TABLE IF NOT EXISTS app_settings (
        id SERIAL PRIMARY KEY,
        key VARCHAR(50) UNIQUE NOT NULL,
        value TEXT NOT NULL,
        description TEXT
    );
    """))
    
    # 2. Master Data Table (Categories)
    db.session.execute(text("""
    CREATE TABLE IF NOT EXISTS master_data (
        id SERIAL PRIMARY KEY,
        category VARCHAR(50) NOT NULL, -- EXPENSE_CATEGORY, HOUSE_TYPE, WING
        label VARCHAR(100) NOT NULL,
        value VARCHAR(100) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        UNIQUE(category, value)
    );
    """))
    
    # Seed some initial data
    db.session.execute(text("""
        INSERT INTO app_settings (key, value, description) VALUES 
        ('app_name', 'SocietyPro', 'The name of the application'),
        ('currency', '$', 'Currency symbol used in the app')
        ON CONFLICT (key) DO NOTHING;
        
        INSERT INTO master_data (category, label, value) VALUES 
        ('EXPENSE_CATEGORY', 'Security', 'Security'),
        ('EXPENSE_CATEGORY', 'Maintenance', 'Maintenance'),
        ('EXPENSE_CATEGORY', 'Electricity', 'Electricity'),
        ('EXPENSE_CATEGORY', 'Water', 'Water'),
        ('HOUSE_TYPE', '1 BHK', '1BHK'),
        ('HOUSE_TYPE', '2 BHK', '2BHK'),
        ('HOUSE_TYPE', '3 BHK', '3BHK'),
        ('HOUSE_TYPE', 'Villa', 'Villa')
        ON CONFLICT (category, value) DO NOTHING;
    """))
    
    db.session.commit()
    print("Settings and Master Data tables created and seeded.")
