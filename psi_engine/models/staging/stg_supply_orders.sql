with source as (
    select * from {{ source('raw_supply_chain', 'mock_supply_orders') }}
),

cleaned as (
    select
        cast(po_id as integer) as po_id,
        cast(item_id as integer) as product_id,
        cast(store_id as integer) as store_id,

        -- Date Handling
        cast(order_date as date) as order_date,
        cast(expected_arrival_date as date) as expected_arrival_date,
        cast(actual_arrival_date as date) as actual_arrival_date,

        cast(qty_ordered as integer) as qty_ordered,

        -- Standardize Status
        upper(status) as status,

        cast(supplier_id as integer) as supplier_id
    
    from source
)

select * from cleaned