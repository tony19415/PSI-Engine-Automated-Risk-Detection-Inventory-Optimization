with daily_data as (
    select * from {{ ref('int_psi_timeline') }}
),

regions as (
    select * from {{ ref('dim_store_regions_hashed') }}
)

select
    -- 1. IDs & Date
    -- We map 'date' from the intermediate layer to 'sale_date' here for clarity
    d.date as sale_date,
    d.product_id,
    d.store_id,
    
    -- 2. Dimensions (From the Join)
    r.region,
    -- Security columns
    r.real_manager_name,
    r.manager_key,
    r.manager_masked,
    
    -- 3. Metrics (Already calculated in int_psi_timeline)
    d.demand as qty_sold,
    d.supply as qty_ordered,
    d.projected_inventory_on_hand,
    
    -- DAMA Auditability: Track when this record was processed by the pipeline
    current_timestamp as dw_inserted_at,
    
    -- 4. Logic (The Health Status)
    case 
        when d.projected_inventory_on_hand < 0 then 'Stockout'
        when d.projected_inventory_on_hand < 10 then 'Risk'
        else 'Healthy'
    end as inventory_health_status

from daily_data d
-- Join Region info onto the main timeline
left join regions r 
    on cast(d.store_id as int) = cast(r.store_id as int)