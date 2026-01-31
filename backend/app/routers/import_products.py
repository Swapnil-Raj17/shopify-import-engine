# from fastapi import APIRouter, UploadFile, File
# from app.services.parser import parse_file
# from app.services.shopify import find_product_by_handle, find_product_by_id, update_product, create_product
# from app.services.merge import merge_product
# import csv
# from io import StringIO
# import traceback
# import sys

# router = APIRouter()

# # Safe CSV parser
# def parse_csv_file(file: UploadFile):
#     try:
#         contents = file.file.read().decode("utf-8")
#         file.file.close()
#         reader = csv.DictReader(StringIO(contents))
#         return [row for row in reader]
#     except Exception as e:
#         raise ValueError(f"Failed to parse CSV: {e}")

# @router.post("/import/products")
# async def import_products(file: UploadFile = File(...)):
#     try:
#         products = parse_csv_file(file)
#         results = []

#         for product in products:
#             try:
#                 # Product identification logic:
#                 # 1. ID
#                 # 2. Handle
#                 # 3. Fallback title
#                 existing = None
#                 if product.get("ID"):
#                     existing = find_product_by_id(product["ID"])
#                 if not existing and product.get("Handle"):
#                     matches = find_product_by_handle(product["Handle"])
#                     if len(matches) == 1:
#                         existing = matches[0]
#                     elif len(matches) > 1:
#                         # Ambiguous handle
#                         existing = None

#                 if existing:
#                     updated = merge_product(existing, product)
#                     update_product(existing["id"], updated)
#                     results.append({"product": product.get("Handle", product.get("Title", "unknown")), "status": "updated"})
#                 else:
#                     create_product(product)
#                     results.append({"product": product.get("Handle", product.get("Title", "unknown")), "status": "created"})

#             except Exception as e:
#                 results.append({
#                     "product": product.get("Handle", product.get("Title", "unknown")),
#                     "status": "error",
#                     "detail": str(e)
#                 })

#         return {"result": results}

#     except Exception as e:
#         traceback.print_exc(file=sys.stdout)
#         return {"error": str(e)}

# from fastapi import APIRouter, UploadFile, File, HTTPException
# from app.services.shopify import (
#     find_product_by_handle,
#     find_product_by_id,
#     update_product,
#     create_product
# )
# from app.services.merge import merge_product
# import csv
# from io import StringIO
# import traceback
# import sys

# router = APIRouter()

# # ======================================================
# # TEMP STORAGE (FOR EDITING BEFORE SAVE)
# # ======================================================
# TEMP_PRODUCTS = {}

# # ======================================================
# # CSV PARSER
# # ======================================================
# def parse_csv_file(file: UploadFile):
#     try:
#         contents = file.file.read().decode("utf-8")
#         file.file.close()
#         reader = csv.DictReader(StringIO(contents))
#         return [row for row in reader]
#     except Exception as e:
#         raise ValueError(f"Failed to parse CSV: {e}")

# # ======================================================
# # POST — IMPORT CSV (UPLOAD)
# # ======================================================
# @router.post("/import/products")
# async def import_products(file: UploadFile = File(...)):
#     try:
#         products = parse_csv_file(file)

#         TEMP_PRODUCTS.clear()
#         for i, p in enumerate(products):
#             TEMP_PRODUCTS[i] = p

#         results = []

#         for product in products:
#             try:
#                 existing = None

#                 # Priority 1: ID
#                 if product.get("ID"):
#                     existing = find_product_by_id(product["ID"])

#                 # Priority 2: Handle
#                 if not existing and product.get("Handle"):
#                     matches = find_product_by_handle(product["Handle"])
#                     if len(matches) == 1:
#                         existing = matches[0]

#                 if existing:
#                     updated = merge_product(existing, product)
#                     update_product(existing["id"], updated)
#                     results.append({
#                         "product": product.get("Handle", product.get("Title", "unknown")),
#                         "status": "updated"
#                     })
#                 else:
#                     create_product(product)
#                     results.append({
#                         "product": product.get("Handle", product.get("Title", "unknown")),
#                         "status": "created"
#                     })

#             except Exception as e:
#                 results.append({
#                     "product": product.get("Handle", product.get("Title", "unknown")),
#                     "status": "error",
#                     "detail": str(e)
#                 })

#         return {
#             "result": results,
#             "editable_records": list(TEMP_PRODUCTS.keys())
#         }

#     except Exception as e:
#         traceback.print_exc(file=sys.stdout)
#         return {"error": str(e)}

# # ======================================================
# # GET — VIEW EDITABLE PRODUCT
# # ======================================================
# @router.get("/import/products/{index}")
# def get_editable_product(index: int):
#     if index not in TEMP_PRODUCTS:
#         raise HTTPException(status_code=404, detail="Product not found")

#     return TEMP_PRODUCTS[index]

# # ======================================================
# # PUT — EDIT PRODUCT (NO SHOPIFY CALL YET)
# # ======================================================
# @router.put("/import/products/{index}")
# def update_editable_product(index: int, payload: dict):
#     if index not in TEMP_PRODUCTS:
#         raise HTTPException(status_code=404, detail="Product not found")

#     TEMP_PRODUCTS[index] = payload

#     return {
#         "status": "updated",
#         "product": payload.get("Handle", payload.get("Title", "unknown"))
#     }

# # ======================================================
# # POST — SAVE EDITED PRODUCT TO SHOPIFY
# # ======================================================
# @router.post("/import/products/{index}/save")
# def save_product_to_shopify(index: int):
#     if index not in TEMP_PRODUCTS:
#         raise HTTPException(status_code=404, detail="Product not found")

#     product = TEMP_PRODUCTS[index]

#     existing = None

#     if product.get("ID"):
#         existing = find_product_by_id(product["ID"])

#     if not existing and product.get("Handle"):
#         matches = find_product_by_handle(product["Handle"])
#         if matches:
#             existing = matches[0]

#     if existing:
#         updated = merge_product(existing, product)
#         update_product(existing["id"], updated)
#         return {"status": "updated"}

#     else:
#         create_product(product)
#         return {"status": "created"}

# # ======================================================
# # GET — FETCH ALL SHOPIFY PRODUCTS
# # ======================================================
# @router.get("/products")
# def get_products():
#     from app.services.shopify import safe_request
#     from app.config import SHOPIFY_BASE_URL

#     url = f"{SHOPIFY_BASE_URL}/products.json"
#     data = safe_request("GET", url)

#     return {
#         "count": len(data.get("products", [])),
#         "products": data.get("products", [])
#     }

# # ======================================================
# # PUT — DIRECT UPDATE TO SHOPIFY
# # ======================================================
# @router.put("/products/{product_id}")
# def update_product_api(product_id: int, payload: dict):
#     updated = update_product(product_id, payload)

#     if not updated:
#         raise HTTPException(status_code=400, detail="Update failed")

#     return {
#         "product": product_id,
#         "status": "updated"
#     }

from fastapi import APIRouter, UploadFile, File, Body, HTTPException
from app.services.shopify import (
    find_product_by_handle,
    find_product_by_id,
    update_product,
    create_product
)
import csv
from io import StringIO

router = APIRouter()

TEMP_PRODUCTS = []


# ---------------- CSV UPLOAD ----------------
@router.post("/import/products")
async def import_products(file: UploadFile = File(...)):
    global TEMP_PRODUCTS

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(StringIO(content))
    TEMP_PRODUCTS = list(reader)

    return {
        "message": "File uploaded successfully",
        "editable_records": list(range(len(TEMP_PRODUCTS)))
    }


# ---------------- GET EDITABLE PRODUCT ----------------
@router.get("/import/products/{index}")
def get_product(index: int):
    if index >= len(TEMP_PRODUCTS):
        raise HTTPException(status_code=404, detail="Product not found")
    return TEMP_PRODUCTS[index]


# ---------------- UPDATE PRODUCT (FRONTEND EDIT) ----------------
@router.put("/import/products/{index}")
def update_temp_product(index: int, payload: dict):
    if index >= len(TEMP_PRODUCTS):
        raise HTTPException(status_code=404, detail="Product not found")

    TEMP_PRODUCTS[index].update(payload)
    return {"message": "Product updated"}


# ---------------- SAVE TO SHOPIFY ----------------
@router.post("/import/products/{index}/save")
def save_to_shopify(index: int):
    if index >= len(TEMP_PRODUCTS):
        raise HTTPException(status_code=404, detail="Product not found")

    product = TEMP_PRODUCTS[index]

    existing = None

    if product.get("ID"):
        existing = find_product_by_id(product["ID"])

    if not existing and product.get("Handle"):
        matches = find_product_by_handle(product["Handle"])
        if len(matches) == 1:
            existing = matches[0]

    if existing:
        update_product(existing["id"], product)
        return {"product": product.get("Handle"), "status": "updated"}

    create_product(product)
    return {"product": product.get("Handle"), "status": "created"}
