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
