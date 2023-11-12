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


CREATE TABLE IF NOT EXISTS stop (
    id VARCHAR(255),
    name VARCHAR(255),
    type VARCHAR(255),
    event VARCHAR(255),
    address VARCHAR(255),
    at_street VARCHAR(255),
    on_street VARCHAR(255),
    municipality VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    parent_station_id VARCHAR(255),
    parent_station_type VARCHAR(255),
    parent_station VARCHAR(255),
    location_type VARCHAR(255),
    zone_id VARCHAR(255),
    platform_code VARCHAR(255),
    platform_name VARCHAR(255),
    vehicle_type VARCHAR(255),
    wheelchair_boarding INTEGER,
    facilities_self VARCHAR(255),
    description VARCHAR(255),
    self VARCHAR(255),
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS trip (
    id VARCHAR(255),
    name VARCHAR(255),
    type VARCHAR(255),
    event VARCHAR(255),
    route_id VARCHAR(255),
    route_type VARCHAR(255),
    route_pattern_id VARCHAR(255),
    route_pattern_type VARCHAR(255),
    service_id VARCHAR(255),
    service_type VARCHAR(255),
    shape_id VARCHAR(255),
    shape_type VARCHAR(255),
    block_id VARCHAR(255),
    direction_id INTEGER,
    headsign VARCHAR(255),
    bikes_allowed INTEGER,
    wheelchair_accessible INTEGER,
    self VARCHAR(255),
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS schedule (
    id VARCHAR(255),
    type VARCHAR(255),
    event VARCHAR(255),
    trip_id VARCHAR(255),
    trip_type VARCHAR(255),
    route_id VARCHAR(255),
    route_type VARCHAR(255),
    stop_id VARCHAR(255),
    stop_type VARCHAR(255),
    arrival_time TIMESTAMP,
    departure_time TIMESTAMP,
    direction_id INTEGER,
    stop_headsign VARCHAR(255),
    stop_sequence INTEGER,
    pickup_type INTEGER,
    drop_off_type INTEGER,
    timepoint BOOLEAN,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS vehicle (
    id VARCHAR(255),
    label VARCHAR(255),
    type VARCHAR(255),
    event VARCHAR(255),
    route_type VARCHAR(255),
    stop_id VARCHAR(255),
    stop_type VARCHAR(255),
    trip_id VARCHAR(255),
    trip_type VARCHAR(255),
    bearing INTEGER,
    current_status VARCHAR(255),
    current_stop_sequence INTEGER,
    direction_id INTEGER,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    speed DOUBLE PRECISION,
    updated_at TIMESTAMP,
    self VARCHAR(255),
    PRIMARY KEY (id)
);



CREATE TABLE IF NOT EXISTS route (
    id VARCHAR(255),
    event VARCHAR(255),
    long_name VARCHAR(255),
    short_name VARCHAR(255),
    type INTEGER,
    color CHAR(7),
    text_color CHAR(7),
    description VARCHAR(255),
    direction_destinations TEXT[],
    direction_names TEXT[],
    fare_class VARCHAR(255),
    short_order INT,
    line_id VARCHAR(255),
    line_type VARCHAR(255),
    self VARCHAR(255),
    PRIMARY KEY (id)
);
