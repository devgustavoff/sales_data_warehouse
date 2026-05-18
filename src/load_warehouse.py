from sqlalchemy import create_engine
import pandas as pd
import os
from logger import get_logger

logger = get_logger(__name__)

def load_warehouse(clean_datas):
    try:
        logger.info("Data load start...")        
        engine = create_engine(os.getenv("DATABASE_URL"))

        clean_datas["dim_customer"].to_sql("dim_customer", con=engine, index=False, if_exists="append")
        clean_datas["dim_product"].to_sql("dim_product", con=engine, index=False, if_exists="append")
        clean_datas["dim_location"].to_sql("dim_location", con=engine, index=False, if_exists="append")
        clean_datas["dim_date"].to_sql("dim_date", con=engine, index=False, if_exists="append")

        dim_customer = pd.read_sql_table("dim_customer", con=engine)
        dim_product = pd.read_sql_table("dim_product", con=engine)
        dim_location = pd.read_sql_table("dim_location", con=engine)
        dim_date = pd.read_sql_table("dim_date", con=engine)

        fact_sales = clean_datas["fact_sales"]
        fact_sales = pd.merge(fact_sales, dim_customer, left_on="Customer ID", right_on="customer_code", how='inner')
        fact_sales = pd.merge(fact_sales, dim_product, left_on="Product ID", right_on="product_code", how='inner')
        fact_sales = pd.merge(fact_sales, dim_location, left_on=["Country", "City", "State", "Region"], right_on=["country", "city", "state", "region"], how='inner')
        fact_sales = pd.merge(fact_sales, dim_date, left_on="Order Date", right_on="date", how='inner')

        fact_sales = fact_sales[["Order ID", "customer_id", "product_id", "location_id", "date_id", "Sales", "Quantity", "Discount", "Profit"]]

        fact_sales = fact_sales.rename(
            columns = {
                "Order ID": "order_id",
                "Sales": "sales",
                "Quantity": "quantity",
                "Discount": "discount",
                "Profit": "profit"
            }
        )

        fact_sales.to_sql("fact_sales", con=engine, index=False, if_exists='append')

        logger.info("Data load concluded")
    
    except Exception as e:
        logger.error(f"Ocurred some error: {e}")
        raise