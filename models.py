from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class PurchaseLink:
    href: str

@dataclass
class Product:
    id: str
    name: str
    price: str
    discount: Optional[str] = None
    credit: Optional[str] = None
    old_price: Optional[str] = None
    review_count: int = 0
    rating: float = 0.0
    product_images: List[str] = field(default_factory=list)
    purchase_link: Optional[PurchaseLink] = None
    merchant_name: Optional[str] = None
    merchant_logo: Optional[str] = None
    screen_size: Optional[str] = None
    storage: Optional[str] = None
    ram: Optional[str] = None