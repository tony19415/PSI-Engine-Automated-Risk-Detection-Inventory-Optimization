-- {{ config(materialized='table') }}

with source as (
    select * from {{ source('raw_supply_chain', 'train') }}
    -- select * from main_raw.train
)

select
    -- Generate unique ID for every sale row if one doesn't exist
    {{ dbt_utils.generate_surrogate_key(['date', 'store', 'item']) }} as sales_id,

    -- Standardize column name
    cast(date as date) as sale_date,
    cast(store as integer) as store_id,
    cast(item as integer) as product_id,
    cast(sales as integer) as qty_sold

from source