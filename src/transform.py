import pandas as pd
from logger import get_logger

logger = get_logger(__name__)

def transform(dirty_datas):
    try:
        logger.info("Data transform start...")
        dim_customer = dirty_datas[["Customer ID", "Customer Name", "Segment"]].drop_duplicates()
        dim_customer = dim_customer.dropna()
        dim_customer = dim_customer.rename(
            columns = {
                "Customer ID": "customer_code",
                "Customer Name": "customer_name",
                "Segment": "segment"
            })
    
        dim_product = dirty_datas[["Product ID", "Category", "Sub-Category", "Product Name"]].drop_duplicates()
        dim_product = dim_product.dropna()
        dim_product = dim_product.rename(
            columns = {
                "Product ID": "product_code",
                "Category": "category",
                "Sub-Category": "sub_category",
                "Product Name": "product_name"
            }
        )

        dim_location = dirty_datas[["Country", "City", "State", "Region"]].drop_duplicates()
        dim_location = dim_location.dropna()
        dim_location = dim_location.rename(
            columns = {
                "Country": "country",
                "City": "city",
                "State": "state",
                "Region": "region"
            }
        )

        dim_date = dirty_datas["Order Date"]
        dim_date = pd.to_datetime(dim_date)
        dim_date = dim_date.drop_duplicates()
        dim_date = dim_date.dropna()
        dim_date = pd.DataFrame({
            "date": dim_date,
            "day_of_week": dim_date.dt.day_name(),
            "month": dim_date.dt.month,
            "quarter": dim_date.dt.quarter,
            "year": dim_date.dt.year,
            "is_holiday": False
        })

        fact_sales = dirty_datas[["Order ID", "Customer ID", "Product ID", "Country", "City", "State", "Region" ,"Order Date", "Sales", "Quantity", "Discount", "Profit"]]
        fact_sales = fact_sales.drop_duplicates(subset=["Order ID", "Product ID"])
        fact_sales["Order Date"] = pd.to_datetime(fact_sales["Order Date"])
        
        logger.info("Data transform concluded")
        
        return {
            "dim_customer": dim_customer,
            "dim_product": dim_product,
            "dim_location": dim_location,
            "dim_date": dim_date,
            "fact_sales": fact_sales
        }
    
    except Exception as e:
        logger.error(f"Ocurred some error: {e}")
        raise