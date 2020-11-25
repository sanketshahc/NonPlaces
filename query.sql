-- for use in CARTO DB
select * from (
    select * from (
      select
        (row_number() over (order by cartodb_id asc)) as cartodb_id,
        the_geom,
        the_geom_webmercator
      from
        "ss-cornell".routes
      ) as t1
  	full join (
      select
        (row_number() over (order by cartodb_id asc)) as bn,
        id,
        vendor_id,
        to_date(to_char(pickup_datetime, 'DD Mon YYYY'),'DD Mon YYYY') as pickup_date,
        to_timestamp(to_char(pickup_datetime, 'HH24:MI:SS'),'HH24:MI:SS')::TIME as pickup_time,
        passenger_count,
        pickup_longitude,
        pickup_latitude,
        dropoff_longitude,
        dropoff_latitude,
        store_and_fwd_flag
      from "ss-cornell".data_1996
 	) as t2
on
t1.cartodb_id = t2.bn
) as joined1

UNION ALL

select * from (
  select * from (
    select
      (row_number() over (order by cartodb_id asc)) as cartodb_id,
      the_geom,
      the_geom_webmercator
    from
      "ss-cornell".routes2
    ) as t1
  full join (
    select
      (row_number() over (order by cartodb_id asc)) as bn,
      id,
      vendor_id,
      to_date(to_char(pickup_datetime, 'DD Mon YYYY'),'DD Mon YYYY') as pickup_date,
      to_timestamp(to_char(pickup_datetime, 'HH24:MI:SS'),'HH24:MI:SS')::TIME as pickup_time,
      passenger_count,
      pickup_longitude,
      pickup_latitude,
      dropoff_longitude,
      dropoff_latitude,
      store_and_fwd_flag
    from "ss-cornell".data_3998
  ) as t2

on

t1.cartodb_id = t2.bn
) as joined2