{{
    config(
        materialized= 'table'
    )
}}

select * from {{source('greenery','users')}}