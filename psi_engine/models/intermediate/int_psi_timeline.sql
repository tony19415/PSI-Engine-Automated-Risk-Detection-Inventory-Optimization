with daily_demand as(
    select
        product_id,
        sale_date,
        sum(qty_sold) as forecasted_demand
    from {{ ref('stg_sales') }}
    where sale_date >= current_date
    group by 1, 2
),

daily_supply as (
    select
        item_id as product_id,
        expected_arrival_date as supply_date,
        sum(qty_ordered) as incoming_supply
    from {{ ref('stg_supply_orders') }}
    where status = 'Open'
    group by 1, 2
),

current_inv as (
    select product_id, qty_on_hand as initial_stock
    from {{ ref('stg_iventory') }}
),

joined as (
    select
        d.sale_date,
        d.product_id,
        coalesce(c.initial_stock, 0) as starting_inventory,
        coalesce(d.forecasted_demand, 0) as demand,
        coalesce(s.incoming_supply, 0) as supply
    from daily_demand d
    left join daily_supply s
        on d.product_id = s.product_id and d.sale_date = s.supply_date
    left join current_inv c
        on d.product_id = c.product_id
)

select
    *,
    starting_inventory
    + sum(supply) over (partition by product_id order by sale_date rows between unbounded preceding and current row)
    - sum(demand) over (partition by product_id order by sale_date rows between unbounded preceding and current row)
    as projected_inventory_on_hand
from joined