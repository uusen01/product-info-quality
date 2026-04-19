import pandas as pd
from database import engine

def main() -> None:
    df = pd.read_sql_table("products", con=engine)
    df.to_csv("products.csv", index=False)

if __name__ == "__main__":
    main()