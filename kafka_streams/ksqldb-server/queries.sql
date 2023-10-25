SET 'auto.offset.reset'='earliest';

/*
  -----------BRONZE DATA LAYER-----------------
  LOAD MBTA KAFKA TOPICS IN KAFKA STREAM
  DEFINE SCHEMA BUT DO NOT APPLY TRANSFORMATIONS
  ----------------------------------------------
*/
CREATE OR REPLACE STREAM VEHICLE_BRONZE (
  id VARCHAR KEY,
  event VARCHAR,
  data STRUCT<
    attributes STRUCT<
      bearing INT,
      carriages ARRAY<STRUCT<
        label VARCHAR,
        occupancy_percentage INT,
        occupancy_status VARCHAR
      >>,
      current_status VARCHAR,
      current_stop_sequence INT,
      direction_id INT,
      label VARCHAR,
      latitude DOUBLE,
      longitude DOUBLE,
      occupancy_status VARCHAR,
      speed INT,
      updated_at VARCHAR
    >,
    id VARCHAR,
    links STRUCT<
      self VARCHAR
    >,
    relationships STRUCT<
      route STRUCT<
        data STRUCT<
          id VARCHAR,
          type VARCHAR
        >
      >,
      stop STRUCT<
        data STRUCT<
          id VARCHAR,
          type VARCHAR
        >
      >,
      trip STRUCT<
        data STRUCT<
          id VARCHAR,
          type VARCHAR
        >
      >
    >,
    type VARCHAR
  >
) WITH (
  KAFKA_TOPIC = 'vehicle-topic',
  VALUE_FORMAT = 'JSON'
);


CREATE OR REPLACE STREAM TRIP_BRONZE (
  id VARCHAR KEY,
  event STRING,
  data STRUCT<
    attributes STRUCT<
      bikes_allowed INT,
      block_id STRING,
      direction_id INT,
      headsign STRING,
      name STRING,
      wheelchair_accessible INT
    >,
    id STRING,
    links STRUCT<
      self STRING
    >,
    relationships STRUCT<
      shape STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >
      >,
      service STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >
      >,
      route STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >
      >,
      route_pattern STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >
      >
    >,
    type STRING
  >
) WITH (
  KAFKA_TOPIC = 'trip-topic',
  VALUE_FORMAT = 'JSON'
);

CREATE OR REPLACE STREAM STOP_BRONZE (
  id VARCHAR KEY,
  event STRING,
  data STRUCT<
    attributes STRUCT<
      address STRING,
      at_street STRING,
      description STRING,
      latitude DOUBLE,
      location_type INT,
      longitude DOUBLE,
      municipality STRING,
      name STRING,
      on_street STRING,
      platform_code STRING,
      platform_name STRING,
      vehicle_type STRING,
      wheelchair_boarding INT
    >,
    id STRING,
    links STRUCT<
      self STRING
    >,
    relationships STRUCT<
      child_stops ARRAY<STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >>
      >,
      facilities STRUCT<
        self STRING
      >,
      parent_station STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >
      >,
      zone STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >
      >
    >,
    type STRING
  >
) WITH (
  KAFKA_TOPIC = 'stop-topic',
  VALUE_FORMAT = 'JSON'
);

CREATE OR REPLACE STREAM SCHEDULE_BRONZE (
  id VARCHAR KEY,
  event STRING,
  data STRUCT<
    attributes STRUCT<
      arrival_time STRING,
      departure_time STRING,
      direction_id INT,
      drop_off_type INT,
      pickup_type INT,
      stop_headsign STRING,
      stop_sequence INT,
      timepoint BOOLEAN
    >,
    id STRING,
    relationships STRUCT<
      route STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >
      >,
      stop STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >
      >,
      trip STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >
      >
    >,
    type STRING
  >
) WITH (
  KAFKA_TOPIC = 'schedule-topic',
  VALUE_FORMAT = 'JSON'
);

CREATE OR REPLACE STREAM ROUTE_BRONZE (
  id VARCHAR KEY,
  event STRING,
  data STRUCT<
    attributes STRUCT<
      color STRING,
      description STRING,
      direction_destinations ARRAY<STRING>,
      direction_names ARRAY<STRING>,
      fare_class STRING,
      long_name STRING,
      short_name STRING,
      short_order STRING,
      text_color STRING,
      type INT
    >,
    id STRING,
    links STRUCT<
      self STRING
    >,
    relationships STRUCT<
      line STRUCT<
        data STRUCT<
          id STRING,
          type STRING
        >
      >
    >,
    type STRING
  >
) WITH (
  KAFKA_TOPIC = 'route-topic',
  VALUE_FORMAT = 'JSON'
);

CREATE OR REPLACE STREAM SHAPE_BRONZE (
  id VARCHAR KEY,
  event STRING,
  data STRUCT<
    attributes STRUCT<
      polyline STRING
    >,
    id STRING,
    links STRUCT<
      self STRING
    >,
    type STRING
  >
) WITH (
  KAFKA_TOPIC = 'shape-topic',
  VALUE_FORMAT = 'JSON'
);

/*
  -----------SILVER DATA LAYER-----------------
  BRONZE DATA COMES IN NESTED JSON FORMAT
  APPLY TRANSFORMATIONS TO FLATTEN THE DATA
  AND CAST CORRECT COLUMN TYPES
  ----------------------------------------------
*/

CREATE OR REPLACE STREAM VEHICLE_SILVER AS
SELECT
    id,
    event,
    data->attributes->bearing AS bearing,
    data->attributes->current_status AS current_status,
    data->attributes->current_stop_sequence AS current_stop_sequence,
    data->attributes->direction_id AS direction_id,
    data->attributes->label AS label,
    data->attributes->latitude AS latitude,
    data->attributes->longitude AS longitude,
    data->attributes->speed AS speed,
    PARSE_TIMESTAMP(data->attributes->updated_at, 'yyyy-MM-dd''T''HH:mm:ssXXX') AS updated_at,
    data->links->self AS self,
    data->relationships->route->data->id AS route_id,
    data->relationships->route->data->type AS route_type,
    data->relationships->stop->data->id AS stop_id,
    data->relationships->stop->data->type AS stop_type,
    data->relationships->trip->data->id AS trip_id,
    data->relationships->trip->data->type AS trip_type,
    data->type AS type
FROM
    VEHICLE_BRONZE
EMIT CHANGES;


CREATE OR REPLACE STREAM TRIP_SILVER AS
SELECT
    id,
    event,
    data->attributes->bikes_allowed AS bikes_allowed,
    data->attributes->block_id AS block_id,
    data->attributes->direction_id AS direction_id,
    data->attributes->headsign AS headsign,
    data->attributes->name AS name,
    data->attributes->wheelchair_accessible AS wheelchair_accessible,
    data->links->self AS self,
    data->relationships->shape->data->id AS shape_id,
    data->relationships->shape->data->type AS shape_type,
    data->relationships->service->data->id AS service_id,
    data->relationships->service->data->type AS service_type,
    data->relationships->route->data->id AS route_id,
    data->relationships->route->data->type AS route_type,
    data->relationships->route_pattern->data->id AS route_pattern_id,
    data->relationships->route_pattern->data->type AS route_pattern_type,
    data->type AS type
FROM
    TRIP_BRONZE
EMIT CHANGES;


CREATE OR REPLACE STREAM STOP_SILVER AS
SELECT
    id,
    event,
    data->attributes->address AS address,
    data->attributes->at_street AS at_street,
    data->attributes->description AS description,
    data->attributes->latitude AS latitude,
    data->attributes->location_type AS location_type,
    data->attributes->longitude AS longitude,
    data->attributes->municipality AS municipality,
    data->attributes->name AS name,
    data->attributes->on_street AS on_street,
    data->attributes->platform_code AS platform_code,
    data->attributes->platform_name AS platform_name,
    data->attributes->vehicle_type AS vehicle_type,
    data->attributes->wheelchair_boarding AS wheelchair_boarding,
    data->links->self AS self,
    data->relationships->facilities->self AS facilities_self,
    data->relationships->parent_station->data->id AS parent_station_id,
    data->relationships->parent_station->data->type AS parent_station_type,
    data->relationships->zone->data->id AS zone_id,
    data->relationships->zone->data->type AS zone_type,
    data->type AS type
FROM
    STOP_BRONZE
EMIT CHANGES;


CREATE OR REPLACE STREAM SCHEDULE_SILVER AS
SELECT
    id,
    event,
    PARSE_TIMESTAMP(data->attributes->arrival_time, 'yyyy-MM-dd''T''HH:mm:ssXXX') AS arrival_time,
    PARSE_TIMESTAMP(data->attributes->departure_time, 'yyyy-MM-dd''T''HH:mm:ssXXX') AS departure_time,
    data->attributes->direction_id AS direction_id,
    data->attributes->drop_off_type AS drop_off_type,
    data->attributes->pickup_type AS pickup_type,
    data->attributes->stop_headsign AS stop_headsign,
    data->attributes->stop_sequence AS stop_sequence,
    data->attributes->timepoint AS timepoint,
    data->relationships->route->data->id AS route_id,
    data->relationships->route->data->type AS route_type,
    data->relationships->stop->data->id AS stop_id,
    data->relationships->stop->data->type AS stop_type,
    data->relationships->trip->data->id AS trip_id,
    data->relationships->trip->data->type AS trip_type,
    data->type AS type
FROM
    SCHEDULE_BRONZE
EMIT CHANGES;


CREATE OR REPLACE STREAM ROUTE_SILVER AS
SELECT
    id,
    event,
    data->attributes->color AS color,
    data->attributes->description AS description,
    data->attributes->direction_destinations AS direction_destinations,
    data->attributes->direction_names AS direction_names,
    data->attributes->fare_class AS fare_class,
    data->attributes->long_name AS long_name,
    data->attributes->short_name AS short_name,
    data->attributes->short_order AS short_order,
    data->attributes->text_color AS text_color,
    data->attributes->type AS type,
    data->links->self AS self,
    data->relationships->line->data->id AS line_id,
    data->relationships->line->data->type AS line_type
FROM
    ROUTE_BRONZE
EMIT CHANGES;



CREATE OR REPLACE STREAM SHAPE_SILVER AS
SELECT
    id,
    event,
    data->attributes->polyline AS polyline,
    data->links->self AS self,
    data->type
FROM
    SHAPE_BRONZE
EMIT CHANGES;
