from dev3 import create_app
from dev3.bl.user_bl import UserBL

app = create_app()
with app.app_context():
    # Create test users for each role
    roles = ['admin', 'staff', 'resident', 'accountant']
    for role in roles:
        username = f"test_{role}"
        email = f"{role}@test.com"
        password = "password123"
        success, res = UserBL.register(username, email, password, role)
        if success:
            print(f"Created {role}: {username} / {password}")
        else:
            print(f"Failed to create {role}: {res}")
