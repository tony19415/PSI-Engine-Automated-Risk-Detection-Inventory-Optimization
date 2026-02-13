import duckdb
import os

# Check for the database file. 
# It is usually named 'dev.duckdb' or 'psi_supply_chain.duckdb'.
# We will try both to be safe.
db_file = 'dev.duckdb'
if not os.path.exists(db_file):
    db_file = 'psi_supply_chain.duckdb'

if not os.path.exists(db_file):
    print(f"Error: Could not find a .duckdb file. Please check your folder.")
else:
    print(f"Connecting to {db_file}...")
    con = duckdb.connect(db_file)
    
    # Run the export query
    try:
        con.sql("COPY (SELECT * FROM fct_supply_chain_daily) TO 'psi_dashboard_data.csv' (HEADER, DELIMITER ',')")
        print("Success! Data exported to psi_dashboard_data.csv")
    except Exception as e:
        print(f"Error exporting data: {e}")