def merge_product(existing: dict, incoming: dict) -> dict:
    """
    Merge incoming product/variant into existing product.
    - existing: existing Shopify product dict
    - incoming: dict from CSV row
    """
    # Update simple fields for the product
    for field in ["title", "body_html", "vendor", "product_type", "tags"]:
        if incoming.get(field):
            existing[field] = incoming[field]

    # Normalize variants
    existing_variants = existing.get("variants", [])

    # Extract incoming variant info
    incoming_variant = {
        "id": incoming.get("Variant ID"),
        "sku": incoming.get("Variant SKU"),
        "price": float(incoming.get("Variant Price") or 0),
        "compare_at_price": float(incoming.get("Variant Compare At Price") or 0),
        "inventory_qty": int(incoming.get("Variant Inventory Qty") or 0),
        "option1": incoming.get("Option1 Value"),
        "option2": incoming.get("Option2 Value"),
        "option3": incoming.get("Option3 Value"),
        "weight": float(incoming.get("Variant Weight") or 0)
    }

    # Match variant by ID first
    matched_variant = None
    if incoming_variant["id"]:
        for v in existing_variants:
            if v.get("id") == incoming_variant["id"]:
                matched_variant = v
                break

    # Fallback: match by SKU
    if not matched_variant and incoming_variant["sku"]:
        matches = [v for v in existing_variants if v.get("sku") == incoming_variant["sku"]]
        if len(matches) == 1:
            matched_variant = matches[0]
        elif len(matches) > 1:
            # SKU collision, log and pick first
            matched_variant = matches[0]
            print(f"⚠ SKU collision for {incoming_variant['sku']}")

    # Merge or append
    if matched_variant:
        matched_variant.update(incoming_variant)
    else:
        existing_variants.append(incoming_variant)

    existing["variants"] = existing_variants
    return existing
