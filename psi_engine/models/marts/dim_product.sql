with product_sales as (
    select
        product_id,
        sum(qty_sold) as total_lifetime_units
    from {{ ref('stg_sales') }}
    group by 1
),

ranked_products as (
    select
        product_id,
        total_lifetime_units,
        sum(total_lifetime_units) over (order by total_lifetime_units desc) / 
        sum(total_lifetime_units) over () as cumulative_volume_pct
    from product_sales
),

final as(
    select
        product_id,
        'Product ' || product_id as product_name,
        case
            when cumulative_volume_pct <= 0.80 then 'A'
            when cumulative_volume_pct <= 0.95 then 'B'
            else 'C'
        end as abc_class,

        case
            when cumulative_volume_pct <= 0.80 then 14
            else 21
        end as lead_time_days
    
    from ranked_products
)

select * from final