import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product


def get_session() -> Session:
    return SessionLocal()


def load_products(category_filter: str | None = None) -> list[Product]:
    session = get_session()
    try:
        query = session.query(Product)
        if category_filter and category_filter != "all":
            query = query.filter(Product.category == category_filter)
        products = query.order_by(Product.id).all()
        return products
    finally:
        session.close()


def compute_information_score_for_product(product: Product) -> int:
    attributes = product.get_attributes()
    score = 0

    if product.description and len(product.description) >= 80:
        score += 1

    if product.category == "electronics":
        if attributes.get("battery_life_hours") is not None:
            score += 1

    if product.category == "grocery":
        if attributes.get("is_gluten_free") is not None:
            score += 1
        if attributes.get("is_high_fiber") is not None:
            score += 1

    return score


def add_product(
    name: str,
    category: str,
    description: str,
    battery_life_hours: int | None,
    is_gluten_free: bool | None,
    is_high_fiber: bool | None,
    barcode,
    price: str,
) -> None:
    session = get_session()
    try:
        attributes = {}

        if category == "electronics":
            attributes["battery_life_hours"] = battery_life_hours

        if category == "grocery":
            attributes["is_gluten_free"] = is_gluten_free
            attributes["is_high_fiber"] = is_high_fiber

        product = Product(
            name=name,
            category=category,
            description=description,
            barcode=barcode,
            price=price,
        )

        product.set_attributes(attributes)
        product.information_score = compute_information_score_for_product(product)

        session.add(product)
        session.commit()
    finally:
        session.close()


def product_to_dict(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "description": product.description,
        "attributes": product.get_attributes(),
        "information_score": product.information_score,
        "barcode": product.barcode,
        "price": product.price,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
    }


def main() -> None:
    st.set_page_config(page_title="Product Information Quality", layout="wide")

    st.title("Product Information Quality Dashboard")
    st.write(
        "Analyze how complete and clear product information is and identify items that may confuse customers."
    )

    st.sidebar.header("Add New Product")

    with st.sidebar.form("add_product_form"):
        name = st.text_input("Name")
        category = st.selectbox("Category", ["electronics", "grocery"])
        description = st.text_area("Description", height=150)
        barcode = st.text_input("Barcode")
        price = st.text_input("Price")
        battery_life_input = st.text_input("Battery Life (hours, electronics only)")
        gluten_choice = st.selectbox(
            "Gluten-free (grocery only)",
            ["Not applicable", "Yes", "No"],
        )
        fiber_choice = st.selectbox(
            "High in fiber (grocery only)",
            ["Not applicable", "Yes", "No"],
        )
        submitted = st.form_submit_button("Add Product")

    if submitted:
        battery_life_value = None
        battery_input_valid = True

        if battery_life_input.strip():
            try:
                battery_life_value = int(battery_life_input)
            except ValueError:
                battery_input_valid = False
                st.error("Battery life must be a whole number of hours.")

        gluten_value = None
        if gluten_choice == "Yes":
            gluten_value = True
        elif gluten_choice == "No":
            gluten_value = False

        fiber_value = None
        if fiber_choice == "Yes":
            fiber_value = True
        elif fiber_choice == "No":
            fiber_value = False

        if not name or not description or not barcode or not price:
            st.error("Name, description, barcode, and price are required.")
        elif battery_input_valid:
            add_product(
                name=name,
                category=category,
                description=description,
                battery_life_hours=battery_life_value,
                is_gluten_free=gluten_value,
                is_high_fiber=fiber_value,
                barcode=barcode,
                price=price,
            )
            st.success("Product added successfully.")

    st.sidebar.header("Filters")
    category_filter = st.sidebar.selectbox(
        "Filter by category",
        ["all", "electronics", "grocery"],
    )

    products = load_products(category_filter if category_filter != "all" else None)
    product_rows = [product_to_dict(p) for p in products]

    st.subheader("All Products")
    if product_rows:
        st.dataframe(product_rows, use_container_width=True)
    else:
        st.write("No products found.")

    st.subheader("Flagged Products (Potentially Inadequate Information)")
    flagged = [p for p in products if p.information_score < 2]
    flagged_rows = [product_to_dict(p) for p in flagged]

    if flagged_rows:
        st.dataframe(flagged_rows, use_container_width=True)
    else:
        st.write("No products are currently flagged.")


if __name__ == "__main__":
    main()
