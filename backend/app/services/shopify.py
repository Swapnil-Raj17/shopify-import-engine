import requests
from app.config import SHOPIFY_BASE_URL, SHOPIFY_TOKEN
from parse import parse
from parse import search
from parse import findall


HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# ----------------------
# Shopify API Helpers
# ----------------------
def fetch_all_products():
    url = f"{SHOPIFY_BASE_URL}/products.json?limit=250"
    res = requests.get(url, headers=HEADERS)
    return res.json().get("products", [])

def safe_request(method, url, **kwargs):
    try:
        res = requests.request(method, url, **kwargs)
        res.raise_for_status()
        return res.json()
    except requests.HTTPError as e:
        print(f"HTTP error: {e}, Response: {res.text}")
        return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def find_product_by_handle(handle):
    url = f"{SHOPIFY_BASE_URL}/products.json?handle={handle}"
    data = safe_request("GET", url, headers=HEADERS)
    return data.get("products", []) if data else []

def find_product_by_id(product_id):
    url = f"{SHOPIFY_BASE_URL}/products/{product_id}.json"
    data = safe_request("GET", url, headers=HEADERS)
    return data.get("product") if data else None

def create_product(data):
    url = f"{SHOPIFY_BASE_URL}/products.json"
    return safe_request("POST", url, json={"product": data}, headers=HEADERS)

def update_product(product_id, data):
    url = f"{SHOPIFY_BASE_URL}/products/{product_id}.json"
    return safe_request("PUT", url, json={"product": data}, headers=HEADERS)


# ----------------------
# Sync Products Function
# ----------------------
def sync_products(file):
    """
    Parse a CSV/Excel file and sync products with Shopify.

    Returns:
        dict: { "created": [], "updated": [], "failed": [] }
    """
    products = parse_file(file)
    results = {"created": [], "updated": [], "failed": []}

    for product in products:
        product_id = product.get("id")
        handle = product.get("handle")

        # Update by ID if exists
        if product_id:
            existing = find_product_by_id(product_id)
            if existing:
                res = update_product(product_id, product)
                if res:
                    results["updated"].append(product_id)
                else:
                    results["failed"].append(product_id)
                continue

        # Search by handle if no ID
        if handle:
            existing_list = find_product_by_handle(handle)
            if existing_list:
                existing_id = existing_list[0]["id"]
                res = update_product(existing_id, product)
                if res:
                    results["updated"].append(existing_id)
                else:
                    results["failed"].append(handle)
                continue

        # Create new product
        res = create_product(product)
        if res and res.get("product"):
            results["created"].append(res["product"]["id"])
        else:
            results["failed"].append(handle or product_id)

    return results


