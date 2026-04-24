import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dev3.bl.user_bl import UserBL
from dev3.__init__ import create_app

app = create_app()
with app.app_context():
    success, res = UserBL.register("resident", "resident@example.com", "password123", "resident")
    if success:
        print("Resident user created: resident / password123")
    else:
        print(f"Resident user creation failed: {res}")
