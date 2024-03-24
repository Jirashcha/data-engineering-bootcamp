with

source as (

    select * from {{ source('greenery', 'events') }}

)

, renamed_recasted as (

    select
        events_id as events_guid
        , session_id
        , page_url
        , created_at
        , event_type
        , user
        , order
        , product

    from source

)

select * from renamed_recasted