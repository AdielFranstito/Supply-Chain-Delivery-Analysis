-- =========================================
-- DATA CLEANING & FEATURE ENGINEERING
-- =========================================

-- Create cleaned feature table
CREATE OR REPLACE TABLE delivery_features AS
SELECT
    *,
    
    -- Calculate delay days
    "Days for shipping (real)" - 
    "Days for shipment (scheduled)" AS delay_days,

    -- Late flag
    CASE
        WHEN "Days for shipping (real)" >
             "Days for shipment (scheduled)" THEN 1
        ELSE 0
    END AS late_flag

FROM dataco_supplychain
WHERE "Days for shipping (real)" IS NOT NULL
  AND "Days for shipment (scheduled)" IS NOT NULL;


-- =========================================
-- FINAL FACT TABLE FOR BI
-- =========================================

CREATE OR REPLACE TABLE fact_delivery_analysis AS
SELECT
    "Order Id",

    CAST(
        STRPTIME("order date (DateOrders)", '%m/%d/%Y %H:%M')
        AS DATE
    ) AS order_date,

    CAST(
        STRPTIME("shipping date (DateOrders)", '%m/%d/%Y %H:%M')
        AS DATE
    ) AS shipping_date,

    Market,
    "Order Region" AS order_region,
    "Customer Segment",
    "Shipping Mode",
    "Category Name" AS product_category,

    "Days for shipping (real)" AS actual_shipping_days,
    "Days for shipment (scheduled)" AS scheduled_shipping_days,

    -- delivery delay
    "Days for shipping (real)" -
    "Days for shipment (scheduled)" AS delivery_delay_days,

    -- late flag
    CASE
        WHEN "Days for shipping (real)" >
             "Days for shipment (scheduled)" THEN 1
        ELSE 0
    END AS late_flag,

    -- severity bucket
    CASE
        WHEN "Days for shipping (real)" <=
             "Days for shipment (scheduled)"
             THEN 'On Time / Early'
        WHEN "Days for shipping (real)" -
             "Days for shipment (scheduled)" BETWEEN 1 AND 2
             THEN 'Mild Delay (1–2 days)'
        WHEN "Days for shipping (real)" -
             "Days for shipment (scheduled)" BETWEEN 3 AND 5
             THEN 'Moderate Delay (3–5 days)'
        ELSE 'Severe Delay (6+ days)'
    END AS delay_severity,

    Sales,
    "Order Item Total",

    -- lost revenue (only if late)
    CASE
        WHEN "Days for shipping (real)" >
             "Days for shipment (scheduled)"
        THEN "Order Item Total"
        ELSE 0
    END AS lost_revenue

FROM dataco_supplychain;
