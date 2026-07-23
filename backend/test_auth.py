import requests

BASE_URL = "http://localhost:8000/api/auth"
email = "session_test@example.com"
password = "password123"

print("1. Signing up...")
res = requests.post(f"{BASE_URL}/signup", json={"email": email, "password": password})
if res.status_code != 200 and res.status_code != 400:
    print("Signup failed:", res.text)
    exit(1)

print("2. Logging in...")
res = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
if res.status_code != 200:
    print("Login failed:", res.text)
    exit(1)

tokens = res.json()
access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]
print("Login successful. Received tokens.")

print("3. Refreshing token...")
res = requests.post(f"{BASE_URL}/refresh", json={"refresh_token": refresh_token})
if res.status_code != 200:
    print("Refresh failed:", res.text)
    exit(1)
access_token = res.json()["access_token"]
print("Refresh successful.")

print("4. Logging out...")
headers = {"Authorization": f"Bearer {access_token}"}
res = requests.post(f"{BASE_URL}/logout", headers=headers)
if res.status_code != 200:
    print("Logout failed:", res.text)
    exit(1)
print("Logout successful.")

print("5. Attempting to refresh token again (should fail)...")
res = requests.post(f"{BASE_URL}/refresh", json={"refresh_token": refresh_token})
if res.status_code == 401:
    print("Success: Token was properly revoked.")
else:
    print("Failed: Token was NOT revoked!", res.status_code, res.text)

