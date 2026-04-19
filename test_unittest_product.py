import unittest
from models import Product
from seed import compute_information_score


class TestProductModel(unittest.TestCase):
    def setUp(self):
        self.electronics_product = Product(
            name="Test Watch",
            category="electronics",
            description="A" * 100,
            barcode=1234567890123,
            price="$49.99",
        )
        self.electronics_product.set_attributes({"battery_life_hours": 24})

        self.grocery_product = Product(
            name="Test Grocery",
            category="grocery",
            description="B" * 100,
            barcode=9876543210123,
            price="$5.99",
        )
        self.grocery_product.set_attributes(
            {"is_gluten_free": True, "is_high_fiber": True}
        )

    def test_set_and_get_attributes(self):
        data = {"battery_life_hours": 36}
        self.electronics_product.set_attributes(data)
        self.assertEqual(self.electronics_product.get_attributes(), data)

    def test_electronics_information_score(self):
        attrs = self.electronics_product.get_attributes()
        score = compute_information_score(
            self.electronics_product.category,
            self.electronics_product.description,
            attrs,
        )
        self.assertEqual(score, 2)

    def test_grocery_information_score(self):
        attrs = self.grocery_product.get_attributes()
        score = compute_information_score(
            self.grocery_product.category,
            self.grocery_product.description,
            attrs,
        )
        self.assertEqual(score, 3)

    def test_product_has_price(self):
        self.assertEqual(self.electronics_product.price, "$49.99")

    def test_product_has_barcode(self):
        self.assertEqual(self.electronics_product.barcode, 1234567890123)


if __name__ == "__main__":
    unittest.main()