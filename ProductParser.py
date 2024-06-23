import re
from bs4 import BeautifulSoup, Tag
from models import Product, PurchaseLink
from typing import Optional, List

class ProductParser:

    @staticmethod
    def extract_floats_from_string(input_string: str) -> List[float]:
        numbers = re.findall(r'\d+\.?\d*', input_string)
        float_numbers = [float(num) for num in numbers]
        return float_numbers

    @staticmethod
    def extract_product_data(product_div: Tag) -> Product:
        # Extract data
        product_id = product_div.get("data-product-id", 10060024)
        name = product_div.find("a", {"data-test": "product-name-link"}).text.strip()
        price = product_div.find("div", {"data-test": "product-price"}).text.strip()

        # Optional fields
        discount_tag = product_div.find("div", {"data-test": "discount-text"})
        discount = discount_tag.text.strip() if discount_tag else None

        credit_tag = product_div.find("span", {"data-test": "credit-payment"})
        credit = credit_tag.text.strip() if credit_tag else None

        old_price_tag = product_div.find("span", {"data-test": "discount-price"})
        old_price = old_price_tag.text.strip() if old_price_tag else None

        review_count_tag = product_div.find("div", {"class": "catalog-item-review__review-amount"})
        review_count = int(review_count_tag.text.strip()) if review_count_tag else 0

        rating_style = product_div.find("div", {"data-test": "rating-stars-value"})['style']
        rating_values = ProductParser.extract_floats_from_string(rating_style)
        rating = rating_values[0] / 100 * 5 if rating_values else 0  # Convert percentage to rating out of 5

        product_images = [img["src"] for img in product_div.find_all("img", {"data-test": "product-image"})]

        purchase_link_tag = product_div.find("a", {"data-test": "product-name-link"})
        purchase_link = PurchaseLink(href=purchase_link_tag["href"]) if purchase_link_tag else None

        merchant_name_tag = product_div.find("span", {"data-test": "merchant-name"})
        merchant_name = merchant_name_tag.text.strip() if merchant_name_tag else None

        merchant_logo_tag = product_div.find("img", {"data-test": "merchant-logo"})
        merchant_logo = merchant_logo_tag["src"] if merchant_logo_tag else None

        screen_size_tag = product_div.find("span", text="Диагональ экрана, в дюймах:")
        screen_size = screen_size_tag.parent.text.split(': ')[1] if screen_size_tag else None

        storage_tag = product_div.find("span", text="Встроенная память, в ГБ:")
        storage = storage_tag.parent.text.split(': ')[1] if storage_tag else None

        ram_tag = product_div.find("span", text="Оперативная память, в ГБ:")
        ram = ram_tag.parent.text.split(': ')[1] if ram_tag else None

        product = Product(
            id=product_id,
            name=name,
            price=price,
            discount=discount,
            credit=credit,
            old_price=old_price,
            review_count=review_count,
            rating=rating,
            product_images=product_images,
            purchase_link=purchase_link,
            merchant_name=merchant_name,
            merchant_logo=merchant_logo,
            screen_size=screen_size,
            storage=storage,
            ram=ram
        )

        return product