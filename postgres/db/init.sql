/*
Postgres equivalent of CREATE DATABASE IF NOT EXISTS
 */
DO $do$
DECLARE
    db_name text := 'mbta';
BEGIN
    IF EXISTS (
        SELECT
        FROM
            pg_database
        WHERE
            datname = db_name) THEN
    RAISE NOTICE 'Database % Already Exists', db_name;
ELSE
    PERFORM
        dblink_exec('dbname=' || current_database(), 'CREATE DATABASE ' || db_name);
END IF;
END
$do$;

\c mbta;
CREATE EXTENSION IF NOT EXISTS POSTGIS;

CREATE TABLE IF NOT EXISTS alert (
    event VARCHAR(255) NOT NULL,
    id varchar(255) NOT NULL,
    active_period varchar(255),
    banner varchar(255),
    cause varchar(255),
    created_at timestamp,
    description varchar(255),
    effect varchar(255),
    header varchar(255),
    image varchar(255),
    image_alternative_text varchar(255),
    informed_entity varchar(255),
    lifecycle varchar(255),
    service_effect varchar(255),
    severity varchar(255),
    short_header varchar(255),
    timeframe varchar(255),
    updated_at timestamp,
    type VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS shape (
    event VARCHAR(255) NOT NULL,
    id varchar(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    geometry GEOMETRY(LINESTRING),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS stop (
    event VARCHAR(255) NOT NULL,
    id varchar(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    address varchar(255),
    at_street varchar(255),
    description varchar(255),
    latitude float,
    location_type integer,
    longitude float,
    municipality varchar(255),
    name varchar(255),
    on_street varchar(255),
    platform_code varchar(255),
    platform_name varchar(255),
    vehicle_type varchar(255),
    wheelchair_boarding integer,
    zone varchar(255),
    parent_station varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS trip (
    event VARCHAR(255) NOT NULL,
    id varchar(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    bikes_allowed integer,
    block_id varchar(255),
    direction_id integer,
    headsign varchar(255),
    name varchar(255),
    wheelchair_accessible integer,
    shape_id varchar(255),
    service_id varchar(255),
    route_id varchar(255),
    route_pattern_id varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS schedule (
    event VARCHAR(255) NOT NULL,
    id varchar(255) NOT NULL,
    arrival_time timestamp,
    departure_time timestamp,
    direction_id integer,
    drop_off_type integer,
    pickup_type integer,
    stop_headsign varchar(255),
    stop_sequence integer,
    timepoint boolean,
    route_id varchar(255),
    stop_id varchar(255),
    trip_id varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS vehicle (
    id varchar(255) NOT NULL,
    event VARCHAR(255) NOT NULL,
    type VARCHAR(255),
    bearing integer,
    current_status varchar(255) NOT NULL,
    current_stop_sequence integer,
    direction_id integer,
    label varchar(255),
    latitude double precision,
    longitude double precision,
    occupancy_status varchar(255),
    speed integer,
    updated_at timestamp NOT NULL,
    route_id varchar(255),
    stop_id varchar(255),
    trip_id varchar(255)
);
