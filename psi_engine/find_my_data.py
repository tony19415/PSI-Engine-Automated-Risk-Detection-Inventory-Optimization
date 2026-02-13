import duckdb
import os

# Check for database file
db_files = [f for f in os.listdir('.') if f.endswith('.duckdb')]

print(f"Found {len(db_files)} database files: {db_files}\n")

for db in db_files:
    print(f"---Checking {db} ---")
    try:
        con = duckdb.connect(db)
        tables = con.sql("SHOW TABLES").fetchall()

        if len(tables) == 0:
            print(" (Empty - No tables found)")
        else:
            print(f"    Found {len(tables)} tables! Here are the first 5:")
            for t in tables[:5]:
                print(f"    - {t[0]}")
            
            # Check for table
            has_table = any('fct_supply_chain_daily' in t[0] for t in tables)
            if has_table:
                print(f"\n ✅ Winner! This file contains 'fct_supply_chain_daily")
                print(f" use this filename in your export script!")
    except Exception as e:
        print(f" Could not read: {e}")
    print("\n")