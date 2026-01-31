from pydantic import BaseModel
from typing import Optional, List

# -------------------------------
# Variant model for Shopify product variants
# -------------------------------
class Variant(BaseModel):
    id: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    compare_at_price: Optional[float] = None
    inventory_qty: Optional[int] = None
    option1: Optional[str] = None
    option2: Optional[str] = None
    option3: Optional[str] = None
    weight: Optional[float] = None

# -------------------------------
# Product model for Shopify products
# -------------------------------
class Product(BaseModel):
    id: Optional[str] = None
    handle: Optional[str] = None
    title: str
    body_html: Optional[str] = None
    vendor: Optional[str] = None
    product_type: Optional[str] = None
    tags: Optional[str] = None
    variants: List[Variant] = []
