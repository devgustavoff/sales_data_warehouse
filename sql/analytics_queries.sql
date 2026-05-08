-- Total revenue per quarter
SELECT 
    dim_date.quarter, 
    dim_date.year, 
    SUM(fact_sales.sales) as total_revenue
FROM dim_date
JOIN fact_sales ON dim_date.date_id = fact_sales.date_id
GROUP BY dim_date.quarter, dim_date.year
ORDER BY dim_date.quarter, dim_date.year;

-- TOP 10 Products per marge
SELECT 
    dim_product.product_name,
    SUM(fact_sales.profit) / SUM(fact_sales.sales) as margin
FROM dim_product
JOIN fact_sales ON dim_product.product_id = fact_sales.product_id
GROUP BY dim_product.product_name
ORDER BY margin DESC
LIMIT 10;

-- Revenue per region + category
SELECT
    dim_location.region,
    dim_product.category,
    SUM(fact_sales.sales) as revenue
FROM dim_location
JOIN fact_sales ON dim_location.locatio_id = fact_sales.location_id
JOIN dim_product ON dim_product.product_id = fact_sales.product_id
GROUP BY dim_location.region, dim_product.category
ORDER BY revenue DESC;

-- Growth up MoM
WITH revenue_per_month AS (
    SELECT dim_date.month, dim_date.year, SUM(fact_sales.sales) as revenue
    FROM dim_date
    JOIN fact_sales ON dim_date.date_id = fact_sales.date_id
    GROUP BY dim_date.month, dim_date.year
    ORDER BY dim_date.month, dim_date.year
), month_over_month AS (
    SELECT month, year, revenue
        LAG(revenue) OVER(ORDER BY month, year) as prev_revenue
    FROM revenue_per_month
)
SELECT month, year, revenue,
    ((revenue - prev_revenue) / prev_revenue) * 100 as growth_mom
FROM month_over_month;