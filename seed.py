from typing import List
from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product

fake = Faker()

def compute_information_score(category: str, description: str, attributes: dict) -> int:
    score = 0
    if description and len(description) >= 80:
        score += 1

    if category == "electronics":
        if attributes.get("battery_life_hours") is not None:
            score += 1

    if category == "grocery":
        if attributes.get("is_gluten_free") is not None:
            score += 1
        if attributes.get("is_high_fiber") is not None:
            score += 1

    return score

def seed_electronics(session: Session, count: int) -> None:
    for _ in range(count):
        name = f"{fake.word().title()} Smartwatch"
        description = fake.text(max_nb_chars=120)
        battery_life = fake.random_element([None, fake.random_int(min=12, max=72)])
        barcode = fake.ean(length=13)
        price = fake.pricetag()

        attributes = {
            "battery_life_hours": battery_life,
        }

        product = Product(
            name=name,
            category="electronics",
            description=description,
            barcode=barcode,
            price=price,
        )

        product.set_attributes(attributes)
        product.information_score = compute_information_score(
            product.category,
            product.description,
            attributes,
        )

        session.add(product)

def seed_grocery(session: Session, count: int) -> None:
    for _ in range(count):
        name = fake.word().title()
        base_description = fake.sentence(nb_words=10)
        barcode = fake.ean(length=13)
        price = fake.pricetag()

        extra_detail = fake.random_element(
            [
                "",
                " Gluten-free.",
                " High in fiber.",
                " Gluten-free and high in fiber.",
            ]
        )

        description = (base_description + " " + extra_detail).strip()

        is_gluten_free = None
        is_high_fiber = None
    
        if "Gluten-free" in extra_detail:
            is_gluten_free = True

        if "High in fiber" in extra_detail or "high in fiber" in extra_detail:
            is_high_fiber = True
        
        attributes = {
            "is_gluten_free": is_gluten_free,
            "is_high_fiber": is_high_fiber,
        }

        product = Product(
            name=name,
            category="grocery",
            description=description,
            barcode=barcode,
            price=price,
        )

        product.set_attributes(attributes)
        product.information_score = compute_information_score(
            product.category,
            product.description,
            attributes,
        )
        
        session.add(product)

def main() -> None:
    session: Session = SessionLocal()
    try:
        session.query(Product).delete()
        seed_electronics(session, count=10)
        seed_grocery(session, count=15)
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    main()