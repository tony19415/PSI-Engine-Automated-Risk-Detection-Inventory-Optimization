{{
    config(
        materialized = 'table',
    )
}}

with days as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2023-01-01' as date)",
        end_date="cast('2025-01-01' as date)"
    ) }}
)

select
    date_day as date_day
from days