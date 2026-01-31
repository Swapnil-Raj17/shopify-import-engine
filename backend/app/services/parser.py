import pandas as pd
from collections import defaultdict
import math

def parse_file(file):
    # Load the file
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    else:
        df = pd.read_excel(file.file)
    
    # Strip all string columns to remove extra spaces
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Group by Handle (or Title if Handle missing)
    grouped = defaultdict(list)
    for _, row in df.iterrows():
        key = row.get("Handle") or row.get("Title")
        grouped[key].append(row)
    
    products = []

    for key, rows in grouped.items():
        base = rows[0]

        product = {
            "id": base.get("ID") if not pd.isna(base.get("ID")) else None,
            "handle": base.get("Handle") or None,
            "title": base.get("Title") or None,
            "body_html": base.get("Body (HTML)") or base.get("Description") or None,
            "vendor": base.get("Vendor") or None,
            "product_type": base.get("Product Type") or None,
            "tags": base.get("Tags") or None,
            "variants": []
        }

        for r in rows:
            variant = {}

            # Handle numeric fields safely
            def clean_numeric(value, convert_int=False):
                if isinstance(value, float) and math.isnan(value):
                    return None
                if convert_int and value is not None:
                    return int(value)
                return value

            variant["id"] = clean_numeric(r.get("Variant ID"))
            variant["sku"] = r.get("Variant SKU") or None
            variant["price"] = clean_numeric(r.get("Variant Price"))
            variant["compare_at_price"] = clean_numeric(r.get("Variant Compare At Price"))
            variant["inventory_qty"] = clean_numeric(r.get("Variant Inventory Qty"), convert_int=True)
            variant["weight"] = clean_numeric(r.get("Variant Weight"))

            # Handle option values
            variant["option1"] = r.get("Option1 Value") or None
            variant["option2"] = r.get("Option2 Value") or None
            variant["option3"] = r.get("Option3 Value") or None

            product["variants"].append(variant)

        products.append(product)

    return products
