import duckdb

con = duckdb.connect("dataco.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE dataco_supplychain AS
    SELECT *
    FROM read_csv_auto(
        'data/DataCoSupplyChain.csv',
        ignore_errors=true
    );
""")

print(con.execute("SHOW TABLES").fetchall())

result = con.execute("""
    SELECT COUNT(*) FROM dataco_supplychain;
""").fetchone()


print("Total rows loaded:", result[0])

# create feature engineered table
con.execute("""
    CREATE OR REPLACE TABLE delivery_features AS
    SELECT
        *,
        "Days for shipping (real)" - "Days for shipment (scheduled)" AS delay_days,
        CASE
            WHEN "Days for shipping (real)" > "Days for shipment (scheduled)" THEN 1
            ELSE 0
        END AS late_flag
    FROM dataco_supplychain
    WHERE "Days for shipping (real)" IS NOT NULL
      AND "Days for shipment (scheduled)" IS NOT NULL;
""")

# sanity check
check = con.execute("""
    SELECT
        COUNT(*) AS total_orders,
        SUM(late_flag) AS total_late,
        ROUND(100.0 * SUM(late_flag) / COUNT(*), 2) AS late_percentage
    FROM delivery_features;
""").fetchall()

print("Delivery summary:", check)


# LATE FLAG 1=LATE 0= NO
# LATE DELIVERY BY SHIPPING MODE
shipping_mode_analysis = con.execute("""
    SELECT
        "Shipping Mode",
        COUNT(*) AS total_orders,
        SUM(late_flag) AS late_orders,
        ROUND(100.0 * SUM(late_flag) / COUNT(*), 2) AS late_percentage
    FROM delivery_features
    GROUP BY "Shipping Mode"
    ORDER BY late_percentage DESC;
""").fetchall()

print("\nLate Delivery by Shipping Mode:")
for row in shipping_mode_analysis:
    print(row)

# LATE DELIVERY BY MARKET
market_analysis = con.execute("""
    SELECT
        Market,
        COUNT(*) AS total_orders,
        SUM(late_flag) AS late_orders,
        ROUND(100.0 * SUM(late_flag) / COUNT(*), 2) AS late_percentage
    FROM delivery_features
    GROUP BY Market
    ORDER BY late_percentage DESC;
""").fetchall()

print("\nLate Delivery by Market:")
for row in market_analysis:
    print(row)

# LATE DELIVERY BY SEGMENT ANALYSIS
segment_analysis = con.execute("""
    SELECT
        "Customer Segment",
        COUNT(*) AS total_orders,
        SUM(late_flag) AS late_orders,
        ROUND(100.0 * SUM(late_flag) / COUNT(*), 2) AS late_percentage
    FROM delivery_features
    GROUP BY "Customer Segment"
    ORDER BY late_percentage DESC;
""").fetchall()

print("\nLate Delivery by Customer Segment:")
for row in segment_analysis:
    print(row)

delay_stats = con.execute("""
    SELECT
        COUNT(*) AS total_orders,
        ROUND(AVG(delay_days), 2) AS avg_delay_days,
        ROUND(AVG(CASE WHEN delay_days > 0 THEN delay_days END), 2) AS avg_late_delay,
        MAX(delay_days) AS max_delay_days
    FROM delivery_features;
""").fetchall()

print("\nOverall Delivery Delay Stats:")
print(delay_stats)

delay_by_shipping = con.execute("""
    SELECT
        "Shipping Mode",
        COUNT(*) AS total_orders,
        ROUND(AVG(delay_days), 2) AS avg_delay_days,
        ROUND(AVG(CASE WHEN delay_days > 0 THEN delay_days END), 2) AS avg_late_delay
    FROM delivery_features
    GROUP BY "Shipping Mode"
    ORDER BY avg_late_delay DESC;
""").fetchall()

print("\nAverage Delay by Shipping Mode:")
for row in delay_by_shipping:
    print(row)

# LEVEL OF DELAY
delay_distribution = con.execute("""
    SELECT
        CASE
            WHEN delay_days <= 0 THEN 'On Time / Early'
            WHEN delay_days BETWEEN 1 AND 2 THEN '1–2 Days Late'
            WHEN delay_days BETWEEN 3 AND 5 THEN '3–5 Days Late'
            ELSE '6+ Days Late'
        END AS delay_bucket,
        COUNT(*) AS total_orders
    FROM delivery_features
    GROUP BY delay_bucket
    ORDER BY total_orders DESC;
""").fetchall()

print("\nDelay Distribution:")
for row in delay_distribution:
    print(row)

# TOTAL SALES VS LATE SALES
revenue_summary = con.execute("""
    SELECT
        ROUND(SUM(Sales), 2) AS total_revenue,
        ROUND(SUM(CASE WHEN late_flag = 1 THEN Sales END), 2) AS late_delivery_revenue,
        ROUND(
            100.0 * SUM(CASE WHEN late_flag = 1 THEN Sales END) / SUM(Sales),
            2
        ) AS late_revenue_percentage
    FROM delivery_features;
""").fetchall()

print("\nRevenue Summary:")
print(revenue_summary)

# LOST REVENUE BY SHIPPING MODE
lost_revenue_shipping = con.execute("""
    SELECT
        "Shipping Mode",
        ROUND(SUM(Sales), 2) AS total_revenue,
        ROUND(SUM(CASE WHEN late_flag = 1 THEN Sales END), 2) AS late_revenue,
        ROUND(
            100.0 * SUM(CASE WHEN late_flag = 1 THEN Sales END) / SUM(Sales),
            2
        ) AS late_revenue_percentage
    FROM delivery_features
    GROUP BY "Shipping Mode"
    ORDER BY late_revenue_percentage DESC;
""").fetchall()

print("\nLost Revenue by Shipping Mode:")
for row in lost_revenue_shipping:
    print(row)

# LOST REVENUE BY MARKET
lost_revenue_market = con.execute("""
    SELECT
        Market,
        ROUND(SUM(Sales), 2) AS total_revenue,
        ROUND(SUM(CASE WHEN late_flag = 1 THEN Sales END), 2) AS late_revenue,
        ROUND(
            100.0 * SUM(CASE WHEN late_flag = 1 THEN Sales END) / SUM(Sales),
            2
        ) AS late_revenue_percentage
    FROM delivery_features
    GROUP BY Market
    ORDER BY late_revenue_percentage DESC;
""").fetchall()

print("\nLost Revenue by Market:")
for row in lost_revenue_market:
    print(row)

delay_severity_analysis = con.execute("""
    SELECT
        -- Mengelompokkan tingkat keterlambatan berdasarkan jumlah hari
        CASE
            WHEN delay_days <= 0 THEN 'On Time / Early'          -- Tidak telat / lebih cepat
            WHEN delay_days BETWEEN 1 AND 2 THEN 'Mild Delay (1–2 days)'   -- Telat ringan
            WHEN delay_days BETWEEN 3 AND 5 THEN 'Moderate Delay (3–5 days)' -- Telat sedang
            ELSE 'Severe Delay (6+ days)'                        -- Telat parah (jarang terjadi)
        END AS delay_severity,

        COUNT(*) AS total_orders,        -- Jumlah order di tiap kategori keterlambatan
        ROUND(AVG(Sales), 2) AS avg_order_value -- Rata-rata nilai order
    FROM delivery_features
    GROUP BY delay_severity
    ORDER BY total_orders DESC;
""").fetchall()


print("\nDelay Severity Analysis:")
for row in delay_severity_analysis:
    print(row)

order_value_analysis = con.execute("""
    SELECT
        -- Mengelompokkan order berdasarkan nilai penjualan
        CASE
            WHEN Sales < 100 THEN 'Low Value'
            WHEN Sales BETWEEN 100 AND 300 THEN 'Medium Value'
            ELSE 'High Value'
        END AS order_value_group,

        COUNT(*) AS total_orders,        -- Total order per grup
        SUM(late_flag) AS late_orders,   -- Total order yang telat
        ROUND(100.0 * SUM(late_flag) / COUNT(*), 2) AS late_percentage,
        ROUND(AVG(delay_days), 2) AS avg_delay_days
    FROM delivery_features
    GROUP BY order_value_group
    ORDER BY late_percentage DESC;
""").fetchall()


print("\nLate Delivery by Order Value:")
for row in order_value_analysis:
    print(row)

driver_scoring = con.execute("""
    SELECT
        "Shipping Mode" AS driver,       -- Kandidat faktor penyebab
        ROUND(AVG(delay_days), 2) AS avg_delay_days,  -- Rata-rata hari keterlambatan
        ROUND(AVG(late_flag) * 100, 2) AS late_rate   -- Persentase keterlambatan
    FROM delivery_features
    GROUP BY "Shipping Mode"
    ORDER BY late_rate DESC;
""").fetchall()


print("\nKey Driver Scoring (Shipping Mode):")
for row in driver_scoring:
    print(row)

# =========================================
# EXPORT FINAL ANALYTICAL TABLE FOR POWER BI
# =========================================

# Create final fact table for BI consumption
con.execute("""
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

    -- delivery delay calculation
    "Days for shipping (real)" - "Days for shipment (scheduled)" AS delivery_delay_days,

    -- late flag
    CASE 
        WHEN "Days for shipping (real)" > "Days for shipment (scheduled)" THEN 1
        ELSE 0
    END AS late_flag,

    -- delay severity bucket
    CASE
        WHEN "Days for shipping (real)" <= "Days for shipment (scheduled)" THEN 'On Time / Early'
        WHEN "Days for shipping (real)" - "Days for shipment (scheduled)" BETWEEN 1 AND 2 THEN 'Mild Delay (1–2 days)'
        WHEN "Days for shipping (real)" - "Days for shipment (scheduled)" BETWEEN 3 AND 5 THEN 'Moderate Delay (3–5 days)'
        ELSE 'Severe Delay (6+ days)'
    END AS delay_severity,

    Sales,
    "Order Item Total",

    -- lost revenue (only if late)
    CASE
        WHEN "Days for shipping (real)" > "Days for shipment (scheduled)"
        THEN "Order Item Total"
        ELSE 0
    END AS lost_revenue

FROM dataco_supplychain
""")

# cleanup old table
con.execute("DROP TABLE IF EXISTS supply_chain")

# Export to CSV for Power BI
con.execute("""
COPY fact_delivery_analysis
TO 'data/fact_delivery_analysis.csv'
(HEADER, DELIMITER ',')
""")

print(" fact_delivery_analysis.csv exported successfully")


