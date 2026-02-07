import pandas as pd
import numpy as np
import os
from datetime import timedelta

# --- CONFIGURATION ---
DATA_DIR = 'data/raw'
INPUT_FILE = os.path.join(DATA_DIR, 'train.csv')
OUTPUT_INVENTORY = os.path.join(DATA_DIR, 'mock_inventory_snapshot.csv')
OUTPUT_POS = os.path.join(DATA_DIR, 'mock_supply_orders.csv')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)

def load_or_create_sales_data():
    """
    Loads the Kaggle 'Store Item Demand' dataset.
    If not found, generates dummy sales data so the script runs immediately for the portfolio.
    """
    if os.path.exists(INPUT_FILE):
        print(f"Loading real sales data from {INPUT_FILE}...")
        df = pd.read_csv(INPUT_FILE, parse_dates=['date'])
        # Filter to last 2 years to keep file size manageable for portfolio
        max_date = df['date'].max()
        df = df[df['date'] > (max_date - timedelta(days=730))]
        return df
    else:
        print(f"Warning: {INPUT_FILE} not found. Generating DUMMY sales data for demonstration...")
        # Create dummy data: 2 Stores, 5 Items, 365 Days
        dates = pd.date_range(start='2024-01-01', periods=365, freq='D')
        data = []
        for store in [1, 2]:
            for item in [1, 2, 3, 4, 5]:
                for d in dates:
                    # Random sales between 10 and 50 units
                    sales = np.random.randint(10, 50)
                    data.append([d, store, item, sales])
        
        df = pd.DataFrame(data, columns=['date', 'store', 'item', 'sales'])
        df.to_csv(INPUT_FILE, index=False)
        return df

def generate_inventory_snapshot(sales_df):
    """
    Generates a 'Current Inventory' snapshot.
    Logic: Inventory = Randomly between 0.5x and 2x the average monthly demand.
    This simulates some items being overstocked and others being at risk.
    """
    print("Generating Inventory Snapshot...")
    
    # Calculate average daily sales per Store/Item
    avg_sales = sales_df.groupby(['store', 'item'])['sales'].mean().reset_index()
    
    # Snapshot Date is the day after the last sales date
    snapshot_date = sales_df['date'].max() + timedelta(days=1)
    
    inventory_rows = []
    for _, row in avg_sales.iterrows():
        # Random coverage days between 7 (risk) and 45 (safe)
        days_on_hand = np.random.randint(7, 45)
        qty_on_hand = int(row['sales'] * days_on_hand)
        
        inventory_rows.append({
            'snapshot_date': snapshot_date,
            'store_id': row['store'],
            'item_id': row['item'],
            'qty_on_hand': qty_on_hand,
            # Add a 'Stock Location' for extra realism in SQL tasks
            'warehouse_location': np.random.choice(['Zone-A', 'Zone-B', 'Bulk-Storage'])
        })
        
    inv_df = pd.DataFrame(inventory_rows)
    inv_df.to_csv(OUTPUT_INVENTORY, index=False)
    print(f"Saved Inventory Snapshot to {OUTPUT_INVENTORY}")

def generate_purchase_orders(sales_df):
    """
    Generates 'Purchase Orders' (POs).
    1. Past POs (Closed): Arrived in the past to explain how we got current inventory.
    2. Future POs (Open): Arriving soon (to calculate Shortage Risk).
    """
    print("Generating Mock Purchase Orders...")
    
    # Get unique Store/Items
    store_items = sales_df[['store', 'item']].drop_duplicates()
    max_date = sales_df['date'].max()
    
    po_rows = []
    po_id_counter = 10001
    
    for _, row in store_items.iterrows():
        store = row['store']
        item = row['item']
        
        # --- GENERATE PAST ORDERS (Last 3 months) ---
        # Simulate an order every ~14 days
        for i in range(1, 7): 
            order_date = max_date - timedelta(days=i*14)
            lead_time = np.random.randint(10, 25) # Varied lead time (Supply Risk)
            arrival_date = order_date + timedelta(days=lead_time)
            
            qty = np.random.choice([100, 200, 500, 1000]) # Standard order packs
            
            po_rows.append({
                'po_id': po_id_counter,
                'store_id': store,
                'item_id': item,
                'order_date': order_date,
                'qty_ordered': qty,
                'expected_arrival_date': arrival_date,
                'actual_arrival_date': arrival_date + timedelta(days=np.random.randint(-2, 5)), # Some late, some early
                'status': 'Closed',
                'supplier_id': np.random.randint(1, 5)
            })
            po_id_counter += 1

        # --- GENERATE FUTURE OPEN ORDERS (Next 4 weeks) ---
        # Randomly decide if there is an open order or not
        if np.random.random() > 0.3: 
            order_date = max_date - timedelta(days=np.random.randint(1, 10))
            lead_time = np.random.randint(10, 25)
            arrival_date = order_date + timedelta(days=lead_time)
            
            po_rows.append({
                'po_id': po_id_counter,
                'store_id': store,
                'item_id': item,
                'order_date': order_date,
                'qty_ordered': np.random.choice([200, 500]),
                'expected_arrival_date': arrival_date,
                'actual_arrival_date': None, # Not arrived yet
                'status': 'Open',
                'supplier_id': np.random.randint(1, 5)
            })
            po_id_counter += 1

    po_df = pd.DataFrame(po_rows)
    po_df.to_csv(OUTPUT_POS, index=False)
    print(f"Saved Supply Orders to {OUTPUT_POS}")

if __name__ == "__main__":
    print("--- Starting Supply Chain Simulation ---")
    sales_data = load_or_create_sales_data()
    generate_inventory_snapshot(sales_data)
    generate_purchase_orders(sales_data)
    print("--- Simulation Complete. Data ready for dbt. ---")