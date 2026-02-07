
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

with source as (
    select * from {{ source('raw_supply_chain', 'train') }}
),

cleaned as (
    select
        -- Generate unique ID for every sale row if one doesn't exist
        {{ dbt_utils.generate_surrogate_key(['date', 'store', 'item']) }} as sales_id,

        -- Standardize column name
        cast(date as date) as sale_date,
        cast(store as integer) as store_id,
        cast(item as integer) as product_id,
        cast(sales as integer) as qty_sold
    
    from source
)

select * from cleaned

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
