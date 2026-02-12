select
    sale_date,
    product_id,
    projected_inventory_on_hand
from {{ ref('fct_supply_chain_daily') }}
where projected_inventory_on_hand < 0