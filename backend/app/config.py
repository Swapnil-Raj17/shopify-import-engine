import os
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")

SHOPIFY_BASE_URL = f"https://{SHOPIFY_STORE}/admin/api/2024-01"

APP_NAME = "Shopefy Import Engine"  # <-- added for logs / references

