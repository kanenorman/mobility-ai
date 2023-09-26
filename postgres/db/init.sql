/*
Postgres equivalent of CREATE DATABASE IF NOT EXISTS
*/
DO
$do$
DECLARE
   db_name text := 'mbta';
BEGIN
   IF EXISTS (SELECT FROM pg_database WHERE datname = db_name) THEN
      RAISE NOTICE 'Database % Already Exists', db_name;
   ELSE
      PERFORM dblink_exec('dbname=' || current_database()
                        , 'CREATE DATABASE ' || db_name);
   END IF;
END
$do$;



\c mbta;

CREATE EXTENSION IF NOT EXISTS POSTGIS;

CREATE TABLE IF NOT EXISTS alert (
    event VARCHAR(255) NOT NULL,
    id VARCHAR(255) PRIMARY KEY NOT NULL,
    active_period VARCHAR(255),
    banner VARCHAR(255),
    cause VARCHAR(255),
    created_at TIMESTAMP,
    description VARCHAR(255),
    effect VARCHAR(255),
    header VARCHAR(255),
    image VARCHAR(255),
    image_alternative_text VARCHAR(255),
    informed_entity VARCHAR(255),
    lifecycle VARCHAR(255),
    service_effect VARCHAR(255),
    severity VARCHAR(255),
    short_header VARCHAR(255),
    timeframe VARCHAR(255),
    updated_at TIMESTAMP,
    type VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS schedule (
    event VARCHAR(255) NOT NULL,
    id VARCHAR(255) PRIMARY KEY NOT NULL,
    arrival_time TIMESTAMP,
    departure_time TIMESTAMP,
    direction_id INTEGER,
    drop_off_type INTEGER,
    pickup_type INTEGER,
    stop_headsign VARCHAR(255),
    stop_sequence INTEGER,
    timepoint BOOLEAN,
    route_id VARCHAR(255),
    stop_id VARCHAR(255),
    trip_id VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS shape (
    event VARCHAR(255) NOT NULL,
    id VARCHAR(255) PRIMARY KEY NOT NULL,
    type VARCHAR(255) NOT NULL,
    geometry GEOMETRY(LINESTRING)
);

CREATE TABLE IF NOT EXISTS stop (
    event VARCHAR(255) NOT NULL,
    id VARCHAR(255) PRIMARY KEY NOT NULL,
    type VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    at_street VARCHAR(255),
    description VARCHAR(255),
    latitude FLOAT,
    location_type INTEGER,
    longitude FLOAT,
    municipality VARCHAR(255),
    name VARCHAR(255),
    on_street VARCHAR(255),
    platform_code VARCHAR(255),
    platform_name VARCHAR(255),
    vehicle_type VARCHAR(255),
    wheelchair_boarding INTEGER,
    zone VARCHAR(255),
    parent_station VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS trip (
    event VARCHAR(255) NOT NULL,
    id VARCHAR(255) PRIMARY KEY NOT NULL,
    type VARCHAR(255) NOT NULL,
    bikes_allowed INTEGER,
    block_id VARCHAR(255),
    direction_id INTEGER,
    headsign VARCHAR(255),
    name VARCHAR(255),
    wheelchair_accessible INTEGER,
    shape_id VARCHAR(255),
    service_id VARCHAR(255),
    route_id VARCHAR(255),
    route_pattern_id VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS vehicle (
    id VARCHAR(255) NOT NULL,
    event VARCHAR(255) NOT NULL,
    type VARCHAR(255),
    bearing INTEGER,
    current_status VARCHAR(255),
    current_stop_sequence INTEGER,
    direction_id INTEGER,
    label VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    occupancy_status VARCHAR(255),
    speed INTEGER,
    updated_at TIMESTAMP NOT NULL,
    route_id VARCHAR(255),
    stop_id VARCHAR(255),
    trip_id VARCHAR(255)
);
