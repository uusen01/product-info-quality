from models import Product
from seed import compute_information_score


def test_compute_information_score_electronics():
    product = Product(
        name="Pytest Watch",
        category="electronics",
        description="A" * 100,
        barcode=1111111111111,
        price="$99.99",
    )
    product.set_attributes({"battery_life_hours": 48})

    score = compute_information_score(
        product.category,
        product.description,
        product.get_attributes(),
    )

    assert score == 2


def test_compute_information_score_grocery():
    product = Product(
        name="Pytest Grocery",
        category="grocery",
        description="B" * 100,
        barcode=2222222222222,
        price="$3.49",
    )
    product.set_attributes({"is_gluten_free": True, "is_high_fiber": True})

    score = compute_information_score(
        product.category,
        product.description,
        product.get_attributes(),
    )

    assert score == 3


def test_product_price_and_barcode():
    product = Product(
        name="Sample Item",
        category="electronics",
        description="Valid description text" * 5,
        barcode=3333333333333,
        price="$12.99",
    )

    assert product.price == "$12.99"
    assert product.barcode == 3333333333333