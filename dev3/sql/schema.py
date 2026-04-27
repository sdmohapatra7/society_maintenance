# Raw SQL schema to create tables (idempotent)
CREATE_USERS = \
"""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'resident', -- admin, resident, staff
    house_id INTEGER REFERENCES houses(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_BILLS = \
"""
CREATE TABLE IF NOT EXISTS bills (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount NUMERIC(10,2) NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'unpaid',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_COMPLAINTS = \
"""
CREATE TABLE IF NOT EXISTS complaints (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    document_url VARCHAR(255),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_EXPENSES = \
"""
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    category VARCHAR(100),
    expense_date DATE DEFAULT CURRENT_DATE,
    description TEXT,
    receipt_url VARCHAR(255),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_EVENTS = \
"""
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    location VARCHAR(200),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_SOCIETIES = \
"""
CREATE TABLE IF NOT EXISTS societies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    address TEXT,
    registration_no VARCHAR(100),
    contact_email VARCHAR(120),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_HOUSES = \
"""
CREATE TABLE IF NOT EXISTS houses (
    id SERIAL PRIMARY KEY,
    society_id INTEGER NOT NULL REFERENCES societies(id) ON DELETE CASCADE,
    wing VARCHAR(20),
    house_no VARCHAR(20) NOT NULL,
    area_sq_ft NUMERIC(10,2),
    house_type VARCHAR(50),
    resident_name VARCHAR(200),
    resident_email VARCHAR(120),
    resident_phone VARCHAR(20),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_MAINTENANCE_BILLS = \
"""
CREATE TABLE IF NOT EXISTS maintenance_bills (
    id SERIAL PRIMARY KEY,
    house_id INTEGER NOT NULL REFERENCES houses(id) ON DELETE CASCADE,
    bill_month DATE NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    fixed_charge NUMERIC(10,2) DEFAULT 0,
    area_charge NUMERIC(10,2) DEFAULT 0,
    late_fee NUMERIC(10,2) DEFAULT 0,
    other_charges NUMERIC(10,2) DEFAULT 0,
    due_date DATE NOT NULL,
    paid_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'unpaid',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_VISITORS = \
"""
CREATE TABLE IF NOT EXISTS visitors (
    id SERIAL PRIMARY KEY,
    house_id INTEGER REFERENCES houses(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    phone VARCHAR(20),
    purpose VARCHAR(100),
    entry_time TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    exit_time TIMESTAMP WITHOUT TIME ZONE,
    status VARCHAR(20) DEFAULT 'in', -- 'in', 'out'
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_VEHICLES = \
"""
CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    house_id INTEGER REFERENCES houses(id) ON DELETE CASCADE,
    license_plate VARCHAR(50) NOT NULL UNIQUE,
    make_model VARCHAR(100),
    vehicle_type VARCHAR(20), -- 'car', 'bike'
    parking_slot VARCHAR(50),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""
CREATE_ROLES = \
"""
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_ROLE_PERMISSIONS = \
"""
CREATE TABLE IF NOT EXISTS role_permissions (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50) NOT NULL,
    feature_name VARCHAR(100) NOT NULL,
    can_access BOOLEAN DEFAULT FALSE,
    UNIQUE(role, feature_name)
);
"""

CREATE_APP_SETTINGS = \
"""
CREATE TABLE IF NOT EXISTS app_settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_MASTER_DATA = \
"""
CREATE TABLE IF NOT EXISTS master_data (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    label VARCHAR(200) NOT NULL,
    value VARCHAR(200) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
"""

CREATE_TABLE_STATEMENTS = [
    CREATE_SOCIETIES,
    CREATE_HOUSES,
    CREATE_USERS, 
    CREATE_BILLS, 
    CREATE_COMPLAINTS, 
    CREATE_EVENTS,
    CREATE_EXPENSES,
    CREATE_MAINTENANCE_BILLS,
    CREATE_VISITORS,
    CREATE_VEHICLES,
    CREATE_ROLES,
    CREATE_ROLE_PERMISSIONS,
    CREATE_APP_SETTINGS,
    CREATE_MASTER_DATA,
    "ALTER TABLE complaints ADD COLUMN IF NOT EXISTS document_url VARCHAR(255);"
]
