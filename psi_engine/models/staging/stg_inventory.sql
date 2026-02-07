with source as (
    select * from {{ source('raw_supply_chain', 'mock_inventory_snapshot') }}
),

cleaned as (
    select
        {{ dbt_utils.generate_surrogate_key(['store_id', 'item_id', 'snapshot_date']) }} as inventory_id,

        cast(snapshot_date as date) as inventory_date,
        cast(store_id as integer) as store_id,
        cast(item_id as integer) as product_id,

        cast(qty_on_hand as integer) as qty_on_hand,

        cast(warehouse_location as varchar) as warehouse_location

    from source
)

select * from cleaned