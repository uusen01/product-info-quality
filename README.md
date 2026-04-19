# Product Info Quality

This project builds a product information dashboard using Python, SQLite, SQLAlchemy, Streamlit, unittest, and pytest.

## Files
- `models.py` - database model
- `database.py` - database connection
- `seed.py` - seeds product data
- `app.py` - Streamlit dashboard
- `export.py` - exports products to CSV
- `test_unittest_product.py` - unittest tests
- `test_pytest_product.py` - pytest tests

## Run
```bash
python seed.py
streamlit run app.py
pytest
python -m unittest test_unittest_product.py
