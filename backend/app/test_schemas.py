from models.schemas import Product, Variant

print("Testing Pydantic schemas...\n")

# Example variant data
variant_data = {
    "id": "123",
    "sku": "ABC-001",
    "price": 19.99,
    "compare_at_price": 24.99,
    "inventory_qty": 100,
    "option1": "Red"
}

variant = Variant(**variant_data)
print("Variant instance created:")
print(variant, "\n")

# Example product data with one variant
product_data = {
    "id": "001",
    "title": "Cool T-Shirt",
    "variants": [variant_data],
    "vendor": "MyBrand",
    "product_type": "Shirts",
    "tags": "clothing,tshirt"
}

product = Product(**product_data)
print("Product instance created:")
print(product)

