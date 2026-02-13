with daily_demand as(
    select
        product_id,
        store_id,
        sale_date,
        sum(qty_sold) as forecasted_demand
    from {{ ref('stg_sales') }}
    where sale_date >= current_date
    group by product_id, store_id, sale_date
),

daily_supply as (
    select
        product_id,
        store_id,
        expected_arrival_date as supply_date,
        sum(qty_ordered) as incoming_supply
    from {{ ref('stg_supply_orders') }}
    where status = 'Open'
    group by product_id, store_id, supply_date
),

current_inv as (
    select 
        product_id,
        store_id, 
        qty_on_hand as initial_stock
    from {{ ref('stg_inventory') }}
),

-- Old Version
-- joined as (
--     select
--         d.sale_date,
--         d.product_id,
--         coalesce(c.initial_stock, 0) as starting_inventory,
--         coalesce(d.forecasted_demand, 0) as demand,
--         coalesce(s.incoming_supply, 0) as supply
--     from daily_demand d
--     left join daily_supply s
--         on d.product_id = s.product_id and d.sale_date = s.supply_date
--     left join current_inv c
--         on d.product_id = c.product_id
-- )

all_keys as (
    select product_id, store_id, sale_date as date from daily_demand
    union distinct
    select product_id, store_id, supply_date as date from daily_supply
    union distinct
    select product_id, store_id, cast(current_date as date) as date from current_inv
),

joined as (
    select
        k.date as sale_date,
        k.product_id,
        k.store_id,
        coalesce(c.initial_stock, 0) as starting_inventory,
        coalesce(d.forecasted_demand, 0) as demand,
        coalesce(s.incoming_supply, 0) as supply
    from all_keys k

    left join daily_demand d
        on k.product_id = d.product_id
        and k.store_id = d.store_id
        and k.date = d.sale_date
    left join daily_supply s
        on k.product_id = s.product_id
        and k.store_id = s.store_id
        and k.date = s.supply_date
    left join current_inv c
        on k.product_id = c.product_id
        and k.store_id = c.store_id
)

select
    *,
    starting_inventory
    + sum(supply) over (partition by product_id order by sale_date rows between unbounded preceding and current row)
    - sum(demand) over (partition by product_id order by sale_date rows between unbounded preceding and current row)
    as projected_inventory_on_hand
from joined