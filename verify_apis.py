import httpx
import sys
import time
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

def test_api(name: str, method: str, path: str, json: Dict[str, Any] = None, headers: Dict[str, str] = None, data: Dict[str, Any] = None):
    print(f"Testing {name}...", end=" ", flush=True)
    try:
        kwargs = {"headers": headers, "timeout": 15.0, "follow_redirects": True}
        if json: kwargs["json"] = json
        if data: kwargs["data"] = data

        if method == "GET":
            r = httpx.get(f"{BASE_URL}{path}", **kwargs)
        else:
            r = httpx.post(f"{BASE_URL}{path}", **kwargs)
        
        if r.status_code in [200, 201]:
            print("✅")
            return r.json()
        elif r.status_code == 400 and "already registered" in r.text:
            print("✅ (User already exists)")
            return True
        else:
            print(f"❌ (Status: {r.status_code})")
            print(f"Response: {r.text}")
            return None
    except Exception as e:
        print(f"❌ (Error: {e})")
        return None

def run_suite():
    # 1. Registration
    user_email = "verify_test@example.com"
    reg_data = {
        "name": "Verify Test User",
        "email": user_email,
        "password": "securepassword123",
        "role_id": 2 # Customer
    }
    test_api("Registration", "POST", "/auth/register", json=reg_data)

    # 2. Login
    login_data = {"username": user_email, "password": "securepassword123"}
    print("Testing Login...", end=" ", flush=True)
    r = httpx.post(f"{BASE_URL}/auth/login", data=login_data, follow_redirects=True)
    if r.status_code == 200:
        print("✅")
        token = r.json()["access_token"]
    else:
        print(f"❌ (Status: {r.status_code})")
        print(f"Response: {r.text}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Metadata
    test_api("Get Categories", "GET", "/categories")
    test_api("Get Pet Types", "GET", "/pet-types")

    # 4. Listings
    products = test_api("Get Products", "GET", "/products")
    pets = test_api("Get Pets", "GET", "/pets")

    # 5. Cart
    if products and isinstance(products, list) and len(products) > 0:
        p = products[0]
        v_id = None
        if "variants" in p and p["variants"]:
            v_id = p["variants"][0]["id"]
        
        if v_id:
            cart_item = {
                "item_type": "product",
                "product_variant_id": v_id,
                "quantity": 1
            }
            test_api("Add to Cart", "POST", "/cart/", json=cart_item, headers=headers)
        else:
            print("Skipping Add to Cart (no variants found for product)")

    print("\nVerification Suite Completed.")

if __name__ == "__main__":
    run_suite()
