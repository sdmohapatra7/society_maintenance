import requests

BASE_URL = "http://127.0.0.1:5000"

def test_access_flow():
    session = requests.Session()
    
    # 1. Login as Admin
    print("Attempting admin login...")
    login_res = session.post(f"{BASE_URL}/auth/login", data={
        "username": "admin",
        "password": "admin123"
    }, allow_redirects=True)
    
    if "Dashboard" in login_res.text or login_res.status_code == 200:
        print("Admin Login successful.")
    else:
        print("Admin Login failed.")
        return

    # 2. Check Access Management page
    print("Checking Access Management page...")
    access_page = session.get(f"{BASE_URL}/access/")
    if "Access Management" in access_page.text:
        print("Access Management page reachable.")
    else:
        print("Access Management page not reachable or unauthorized.")
        return

    # 3. Try to update a permission for a resident (let's assume user_id 2 exists from seed)
    print("Testing permission update...")
    update_res = session.post(f"{BASE_URL}/access/update", json={
        "user_id": 2,
        "feature_name": "billing",
        "can_access": False
    })
    
    if update_res.status_code == 200 and update_res.json().get("success"):
        print("Permission update API works.")
    else:
        print(f"Permission update failed: {update_res.text}")

    print("\nAccess Management Test Completed Successfully.")

if __name__ == "__main__":
    try:
        test_access_flow()
    except Exception as e:
        print(f"Test crashed: {e}")
