import duckdb

con = duckdb.connect("dataco.duckdb")

# Load raw CSV
con.execute("""
CREATE OR REPLACE TABLE dataco_supplychain AS
SELECT *
FROM read_csv_auto(
    'data/DataCoSupplyChain.csv',
    ignore_errors=true
);
""")

# Run data cleaning SQL
with open("sql/data_cleaning.sql", "r") as f:
    con.execute(f.read())

# Export final table
con.execute("""
COPY fact_delivery_analysis
TO 'data/fact_delivery_analysis.csv'
(HEADER, DELIMITER ',')
""")

print("Pipeline executed successfully.")
