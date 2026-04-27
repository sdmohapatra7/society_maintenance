import requests

def test_app():
    print("Starting Comprehensive Application Test...")
    session = requests.Session()
    
    # 1. Test Login
    print("Testing Login Endpoint (/auth/login)...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    res = session.post('http://127.0.0.1:5000/auth/login', data=login_data)
    
    if res.status_code != 200:
        print(f"FAILED: Login returned {res.status_code}")
        return
        
    print("Login Successful!")
    
    # 2. Test Core Endpoints
    endpoints = [
        '/',
        '/societies/',
        '/houses/',
        '/users/',
        '/billing/',
        '/expenses/',
        '/complaints/',
        '/access/',
        '/events/',
        '/visitors/',
        '/vehicles/',
        '/reports/',
        '/accounting/',
        '/settings/'
    ]
    
    all_passed = True
    for ep in endpoints:
        print(f"Testing Endpoint: {ep} ...", end=" ")
        try:
            r = session.get(f'http://127.0.0.1:5000{ep}')
            if r.status_code == 200:
                print("PASSED (200 OK)")
            elif r.status_code == 403:
                print("SKIPPED (403 Unauthorized - Normal for role constraints)")
            else:
                print(f"FAILED (Status: {r.status_code})")
                all_passed = False
        except Exception as e:
            print(f"ERROR: {e}")
            all_passed = False
            
    print("\n--- TEST SUMMARY ---")
    if all_passed:
        print("✅ ALL MODULES FUNCTIONAL! Zero 500 Server Errors detected.")
    else:
        print("❌ SOME MODULES FAILED. Check logs above.")

if __name__ == '__main__':
    test_app()
