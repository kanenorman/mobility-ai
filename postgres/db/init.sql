/*******************************************************
SQL SCHEMA DEFINITION FOR MOBILITY AI DATABASE

This SQL file defines the schema for the Mobility AI database. 
It includes the creation of tables, extensions, views, 
and indexes necessary to organize and query MBTA-related data.

The schema encompasses tables for stops, trips, schedules, vehicles, 
routes, and location views, with relevant columns and primary keys.
Additionally, indexes are created on key join fields to optimize query performance.

Author: Kane Norman
Date: 2023
*******************************************************/



/*******************************************************
                  DATABSE CREATION
POSTGRES EQUIVALENT OF CREATE DATABASE IF NOT EXISTS
********************************************************/
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

/*****************************
      DATABSE EXTENSIONS
*****************************/

\c mbta;
CREATE EXTENSION IF NOT EXISTS POSTGIS;


/*****************************
       DATABASE TABLES
*****************************/

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
    location_type INTEGER,
    zone_id VARCHAR(255),
    platform_code VARCHAR(255),
    platform_name VARCHAR(255),
    vehicle_type INTEGER,
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
    type VARCHAR(255),
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

/*****************************
        DATABASE INDEXES
*****************************/

CREATE INDEX IF NOT EXISTS idx_schedule_stop_id
ON schedule (stop_id);

CREATE INDEX IF NOT EXISTS idx_schedule_route_id
ON schedule (route_id);

CREATE INDEX IF NOT EXISTS idx_trip_route_id
ON trip (route_id);

CREATE INDEX IF NOT EXISTS idx_vehicle_stop_id
ON vehicle (stop_id);

CREATE INDEX IF NOT EXISTS idx_schedule_trip_id
ON schedule (trip_id);

CREATE INDEX IF NOT EXISTS idx_route_route_id
ON route (route_id);


/*****************************
        DATABASE VIEWS
*****************************/

CREATE OR REPLACE VIEW location AS
WITH cte AS (
    SELECT
        stop.name AS stop_name,
        MIN(stop.longitude) AS longitude,
        MIN(stop.latitude) AS latitude,
        ARRAY(
            SELECT DISTINCT e
            FROM unnest(array_agg(route.color)) AS a(e)
        ) AS colors
    FROM
        schedule
    INNER JOIN
        stop
    ON
        schedule.stop_id = stop.id
    INNER JOIN
        route
    ON
        schedule.route_id = route.id
    WHERE
        stop.vehicle_type IN(0,1,2)
    GROUP BY
        stop.name
)

SELECT
    stop_name,
    longitude,
    latitude,
    CASE
        WHEN array_length(colors, 1) = 2 THEN '#000000'
        ELSE colors[1]
    END AS color
FROM
    cte;
