CREATE TABLE dim_customer(
    customer_id SERIAL PRIMARY KEY,
    customer_code VARCHAR,
    customer_name VARCHAR(255),
    segment VARCHAR(50)
);

CREATE TABLE dim_product(
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR,
    category VARCHAR(50),
    sub_category VARCHAR(50),
    product_name VARCHAR(255)
);

CREATE TABLE dim_location(
    location_id SERIAL PRIMARY KEY,
    country VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    region VARCHAR(50)
);

CREATE TABLE dim_date(
    date_id SERIAL PRIMARY KEY,
    date DATE,
    day_of_week VARCHAR(20),
    month INT,
    quarter INT,
    year INT,
    is_holiday BOOLEAN
);

CREATE TABLE fact_sales(
    order_id VARCHAR,
    customer_id INT,
    product_id INT,
    location_id INT,
    date_id INT,
    sales NUMERIC,
    quantity INT,
    discount NUMERIC,
    profit NUMERIC,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);