select
    t.sale_date,
    t.product_id,
    p.abc_class,
    t.demand,
    t.supply,
    t.projected_inventory_on_hand

    case
        when t.projected_inventory_on_hand < 0 then 'Stockout'
        when t.projected_inventory_on_hand < (p.lead_time * t.demand) then 'Risk'
        else 'Healthy'
    end as inventory_health_status

from {{ ref('init_psi_timeline') }} t
left join {{ ref('dim_product') }} p on t.product_id = p.product_id