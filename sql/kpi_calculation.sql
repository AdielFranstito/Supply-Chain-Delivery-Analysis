-- =========================================
-- KPI CALCULATIONS
-- =========================================

-- Overall delivery performance
SELECT
    COUNT(*) AS total_orders,
    SUM(late_flag) AS total_late_orders,
    ROUND(100.0 * SUM(late_flag) / COUNT(*), 2) AS late_percentage
FROM fact_delivery_analysis;


-- Revenue impact
SELECT
    ROUND(SUM(Sales), 2) AS total_revenue,
    ROUND(SUM(lost_revenue), 2) AS late_delivery_revenue,
    ROUND(
        100.0 * SUM(lost_revenue) / SUM(Sales),
        2
    ) AS late_revenue_percentage
FROM fact_delivery_analysis;


-- Late delivery by shipping mode
SELECT
    "Shipping Mode",
    COUNT(*) AS total_orders,
    SUM(late_flag) AS late_orders,
    ROUND(100.0 * SUM(late_flag) / COUNT(*), 2) AS late_percentage
FROM fact_delivery_analysis
GROUP BY "Shipping Mode"
ORDER BY late_percentage DESC;


-- Late revenue by market
SELECT
    Market,
    ROUND(SUM(Sales), 2) AS total_revenue,
    ROUND(SUM(lost_revenue), 2) AS late_revenue,
    ROUND(
        100.0 * SUM(lost_revenue) / SUM(Sales),
        2
    ) AS late_revenue_percentage
FROM fact_delivery_analysis
GROUP BY Market
ORDER BY late_revenue_percentage DESC;
