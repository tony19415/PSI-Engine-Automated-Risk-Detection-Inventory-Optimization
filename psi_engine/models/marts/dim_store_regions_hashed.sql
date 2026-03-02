with source as (
    select * from {{ ref('dim_store_regions') }}
)

select
    store_id,
    region,

    manager_name as real_manager_name,
    md5(manager_name) as manager_key,
    concat(substr(manager_name, 1, 1), '***') as manager_masked

from source