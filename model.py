from dataclasses import dataclass


@dataclass
class Product:
    id_product: str
    name_product: str
    url_product: str
    brand: str
    actual_price_item: str
    old_price_item: str
