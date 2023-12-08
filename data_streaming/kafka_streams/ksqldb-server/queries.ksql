/****************************************************
            MBTA DATA PROCESSING SCRIPT

This KSQL script is responsible for processing data
related to the Massachusetts Bay Transportation Authority (MBTA).

The script is organized into three data layers:

1. Bronze Data Layer:
   - Loads data from Kafka topics into streams.
   - Defines the schema without applying transformations.

2. Silver Data Layer:
   - Applies transformations to flatten the nested JSON data structure.
   - Casts columns to the correct data types.
   - Registers the resulting schema in the schema registry.

3. Gold Data Layer:
   - Creates tables that store the latest state of data for each key.

Each section is clearly labeled and commented for clarity.

Author: Kane Norman
Date: 2023

****************************************************/

-- CONSUME MESSAGE STARTING FROM BEGINNING
SET 'auto.offset.reset'='earliest';

/****************************************************
  -----------BRONZE DATA LAYER-----------------
  LOAD MBTA KAFKA TOPICS IN KAFKA STREAM
  DEFINE SCHEMA BUT DO NOT APPLY TRANSFORMATIONS

  EXAMPLE:

  TOPIC:

  [
    {
      "id": "foo",
      "event": "update",
      "data": {"spam": "eggs"}
    },
    {
      "id": "bar",
      "event": "add",
      "data": {"spam": "ham"}
    },
  ]

  STREAM:
  ------------------------------------
  | ID   | EVENT   |      DATA       |
  |------|---------|-----------------|
  | foo  | update  | {"spam":"eggs"} |
  | bar  | add     | {"spam":"ham"}  |
  ------------------------------------

****************************************************/

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
      vehicle_type INT,
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

/*****************************************************
  --------------- SILVER DATA LAYER ---------------
  In the Silver Data Layer, incoming bronze data is
  in a nested JSON format. We apply transformations
  to flatten the data structure, cast correct column
  types, and register the resulting schema in JSON
  format in the schema registry.

  EXAMPLE:

  ORIGINAL STREAM:
  -----------------------------------
  | ID |          DATA              |
  |----|----------------------------|
  | 1  |{"foo":"bar", "spam":"eggs"}|
  | 2  |{"foo":"baz", "spam":"ham"} |
  -----------------------------------

  FLATTENED STREAM:
  ---------------------
  | ID |  FOO |  SPAM |
  |----|------|-------|
  | 1  | bar  | eggs  |
  | 2  | baz  | ham   |
  ---------------------

****************************************************/

CREATE OR REPLACE STREAM VEHICLE_SILVER
WITH (VALUE_FORMAT='JSON_SR')
AS
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


CREATE OR REPLACE STREAM TRIP_SILVER
WITH (VALUE_FORMAT='JSON_SR')
AS
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


CREATE OR REPLACE STREAM STOP_SILVER
WITH (VALUE_FORMAT='JSON_SR')
AS
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
    data->type AS type
FROM
    STOP_BRONZE
EMIT CHANGES;


CREATE OR REPLACE STREAM SCHEDULE_SILVER
WITH (VALUE_FORMAT='JSON_SR')
AS
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


CREATE OR REPLACE STREAM ROUTE_SILVER
WITH (VALUE_FORMAT='JSON_SR')
AS
SELECT
    id,
    event,
    '#'+ data->attributes->color AS color,
    data->attributes->description AS description,
    data->attributes->direction_destinations AS direction_destinations,
    data->attributes->direction_names AS direction_names,
    data->attributes->fare_class AS fare_class,
    data->attributes->long_name AS long_name,
    data->attributes->short_name AS short_name,
    data->attributes->short_order AS short_order,
    '#' + data->attributes->text_color AS text_color,
    data->attributes->type AS type,
    data->links->self AS self,
    data->relationships->line->data->id AS line_id,
    data->relationships->line->data->type AS line_type
FROM
    ROUTE_BRONZE
EMIT CHANGES;



CREATE OR REPLACE STREAM SHAPE_SILVER
WITH (VALUE_FORMAT='JSON_SR')
AS
SELECT
    id,
    event,
    data->attributes->polyline AS geometry,
    data->links->self AS self,
    data->type
FROM
    SHAPE_BRONZE
EMIT CHANGES;


/****************************************************
  --------------- GOLD DATA LAYER ---------------
  In the Silver Data Layer, data is saved as a stream,
  which represents an unbounded series of events.
  Each record for a given stream is preserved over time.
  In contrast, the Gold Layer is responsible for creating
  tables that store only the latest state of a given key.

  EXAMPLE:

  STREAM:
  --------------------------------
  | ID | NAME | LOCATION | TIME  |
  |----|------|----------|-------|
  | 1  | JIM  | BOSTON   | 9:00  |
  | 1  | JIM  | NEW YORK | 9:30  |
  | 2  | AMY  | CHICAGO  | 7:00  |
  | 2  | AMY  | MIAMI    | 7:30  |
  --------------------------------

  TABLE:
  --------------------------------
  | ID | NAME | LOCATION | TIME  |
  |----|------|----------|-------|
  | 1  | JIM  | NEW YORK | 9:30  |
  | 2  | AMY  | MIAMI    | 7:30  |
  --------------------------------

****************************************************/


CREATE OR REPLACE TABLE STOP_GOLD
WITH (VALUE_FORMAT='JSON_SR')
AS
SELECT
    id,
    LATEST_BY_OFFSET(event) AS event,
    LATEST_BY_OFFSET(address) AS address,
    LATEST_BY_OFFSET(at_street) AS at_street,
    LATEST_BY_OFFSET(description) AS description,
    LATEST_BY_OFFSET(latitude) AS latitude,
    LATEST_BY_OFFSET(location_type) AS location_type,
    LATEST_BY_OFFSET(longitude) AS longitude,
    LATEST_BY_OFFSET(municipality) AS municipality,
    LATEST_BY_OFFSET(name) AS name,
    LATEST_BY_OFFSET(on_street) AS on_street,
    LATEST_BY_OFFSET(platform_code) AS platform_code,
    LATEST_BY_OFFSET(platform_name) AS platform_name,
    LATEST_BY_OFFSET(vehicle_type) AS vehicle_type,
    LATEST_BY_OFFSET(wheelchair_boarding) AS wheelchair_boarding,
    LATEST_BY_OFFSET(self) AS self,
    LATEST_BY_OFFSET(facilities_self) AS facilities_self,
    LATEST_BY_OFFSET(parent_station_id) AS parent_station_id,
    LATEST_BY_OFFSET(parent_station_type) AS parent_station_type,
    LATEST_BY_OFFSET(zone_id) AS zone_id,
    LATEST_BY_OFFSET(type) AS type
FROM
    STOP_SILVER
GROUP BY
    id
EMIT CHANGES;

CREATE OR REPLACE TABLE VEHICLE_GOLD
WITH (VALUE_FORMAT='JSON_SR')
AS
SELECT
    id,
    LATEST_BY_OFFSET(event) AS event,
    LATEST_BY_OFFSET(bearing) AS bearing,
    LATEST_BY_OFFSET(current_status) AS current_status,
    LATEST_BY_OFFSET(current_stop_sequence) AS current_stop_sequence,
    LATEST_BY_OFFSET(direction_id) AS direction_id,
    LATEST_BY_OFFSET(label) AS label,
    LATEST_BY_OFFSET(latitude) AS latitude,
    LATEST_BY_OFFSET(longitude) AS longitude,
    LATEST_BY_OFFSET(speed) AS speed,
    LATEST_BY_OFFSET(updated_at) AS updated_at,
    LATEST_BY_OFFSET(self) AS self,
    LATEST_BY_OFFSET(stop_id) AS stop_id,
    LATEST_BY_OFFSET(stop_type) AS stop_type,
    LATEST_BY_OFFSET(trip_id) AS trip_id,
    LATEST_BY_OFFSET(trip_type) AS trip_type,
    LATEST_BY_OFFSET(type) AS type
FROM
    VEHICLE_SILVER
GROUP BY
    id
EMIT CHANGES;


CREATE OR REPLACE TABLE SHAPE_GOLD
WITH (VALUE_FORMAT='JSON_SR')
AS
SELECT
    id,
    LATEST_BY_OFFSET(event) AS event,
    LATEST_BY_OFFSET(geometry) AS geometry,
    LATEST_BY_OFFSET(self) AS self,
    LATEST_BY_OFFSET(type) AS type
FROM
    SHAPE_SILVER
GROUP BY
    id
EMIT CHANGES;


CREATE OR REPLACE TABLE ROUTE_GOLD
WITH (VALUE_FORMAT='JSON_SR')
AS
SELECT
    id,
    LATEST_BY_OFFSET(event) AS event,
    LATEST_BY_OFFSET(color) AS color,
    LATEST_BY_OFFSET(description) AS description,
    LATEST_BY_OFFSET(direction_destinations) AS direction_destinations,
    LATEST_BY_OFFSET(direction_names) AS direction_names,
    LATEST_BY_OFFSET(fare_class) AS fare_class,
    LATEST_BY_OFFSET(long_name) AS long_name,
    LATEST_BY_OFFSET(short_name) AS short_name,
    LATEST_BY_OFFSET(short_order) AS short_order,
    LATEST_BY_OFFSET(text_color) AS text_color,
    LATEST_BY_OFFSET(type) AS type,
    LATEST_BY_OFFSET(self) AS self,
    LATEST_BY_OFFSET(line_id) AS line_id,
    LATEST_BY_OFFSET(line_type) AS line_type
FROM
    ROUTE_SILVER
GROUP BY
    id
EMIT CHANGES;

CREATE OR REPLACE TABLE SCHEDULE_GOLD
WITH (VALUE_FORMAT='JSON_SR')
AS
SELECT
    id,
    LATEST_BY_OFFSET(event) AS event,
    LATEST_BY_OFFSET(arrival_time) AS arrival_time,
    LATEST_BY_OFFSET(departure_time) AS departure_time,
    LATEST_BY_OFFSET(direction_id) AS direction_id,
    LATEST_BY_OFFSET(drop_off_type) AS drop_off_type,
    LATEST_BY_OFFSET(pickup_type) AS pickup_type,
    LATEST_BY_OFFSET(stop_headsign) AS stop_headsign,
    LATEST_BY_OFFSET(stop_sequence) AS stop_sequence,
    LATEST_BY_OFFSET(timepoint) AS timepoint,
    LATEST_BY_OFFSET(route_id) AS route_id,
    LATEST_BY_OFFSET(route_type) AS route_type,
    LATEST_BY_OFFSET(stop_id) AS stop_id,
    LATEST_BY_OFFSET(stop_type) AS stop_type,
    LATEST_BY_OFFSET(trip_id) AS trip_id,
    LATEST_BY_OFFSET(trip_type) AS trip_type,
    LATEST_BY_OFFSET(type) AS type
FROM
    SCHEDULE_SILVER
GROUP BY
    id
EMIT CHANGES;



CREATE OR REPLACE TABLE TRIP_GOLD
WITH (VALUE_FORMAT='JSON_SR')
AS
SELECT
    id,
    LATEST_BY_OFFSET(event) AS event,
    LATEST_BY_OFFSET(bikes_allowed) AS bikes_allowed,
    LATEST_BY_OFFSET(block_id) AS block_id,
    LATEST_BY_OFFSET(direction_id) AS direction_id,
    LATEST_BY_OFFSET(headsign) AS headsign,
    LATEST_BY_OFFSET(name) AS name,
    LATEST_BY_OFFSET(wheelchair_accessible) AS wheelchair_accessible,
    LATEST_BY_OFFSET(self) AS self,
    LATEST_BY_OFFSET(shape_id) AS shape_id,
    LATEST_BY_OFFSET(shape_type) AS shape_type,
    LATEST_BY_OFFSET(service_id) AS service_id,
    LATEST_BY_OFFSET(service_type) AS service_type,
    LATEST_BY_OFFSET(route_id) AS route_id,
    LATEST_BY_OFFSET(route_type) AS route_type,
    LATEST_BY_OFFSET(route_pattern_id) AS route_pattern_id,
    LATEST_BY_OFFSET(route_pattern_type) AS route_pattern_type,
    LATEST_BY_OFFSET(type) AS type
FROM
    TRIP_SILVER
GROUP BY
    id
EMIT CHANGES;


/****************************************************
  ------------------ JSON STREAMS --------------------
Spark structured streaming is not (easily) compatible with the
confluent JSON_SR or Avro. Therefore, we must convert
to JSON for downstream processing in Apache Spark.

Relevant Readings:
TITLE: "Why JSON isn’t the same as JSON Schema in Kafka Connect converters and ksqlDB (Viewing Kafka messages bytes as hex)"
LINK: https://rmoff.net/2020/07/03/why-json-isnt-the-same-as-json-schema-in-kafka-connect-converters-and-ksqldb-viewing-kafka-messages-bytes-as-hex/

TITLE: "Integrating Spark Structured Streaming with the Confluent Schema Registry"
LINK: https://stackoverflow.com/questions/48882723/integrating-spark-structured-streaming-with-the-confluent-schema-registry
****************************************************/




CREATE OR REPLACE TABLE STOP_JSON
WITH (VALUE_FORMAT='JSON')
AS
SELECT
    id,
    LATEST_BY_OFFSET(event) AS event,
    LATEST_BY_OFFSET(address) AS address,
    LATEST_BY_OFFSET(at_street) AS at_street,
    LATEST_BY_OFFSET(description) AS description,
    LATEST_BY_OFFSET(latitude) AS latitude,
    LATEST_BY_OFFSET(location_type) AS location_type,
    LATEST_BY_OFFSET(longitude) AS longitude,
    LATEST_BY_OFFSET(municipality) AS municipality,
    LATEST_BY_OFFSET(name) AS name,
    LATEST_BY_OFFSET(on_street) AS on_street,
    LATEST_BY_OFFSET(platform_code) AS platform_code,
    LATEST_BY_OFFSET(platform_name) AS platform_name,
    LATEST_BY_OFFSET(vehicle_type) AS vehicle_type,
    LATEST_BY_OFFSET(wheelchair_boarding) AS wheelchair_boarding,
    LATEST_BY_OFFSET(self) AS self,
    LATEST_BY_OFFSET(facilities_self) AS facilities_self,
    LATEST_BY_OFFSET(parent_station_id) AS parent_station_id,
    LATEST_BY_OFFSET(parent_station_type) AS parent_station_type,
    LATEST_BY_OFFSET(zone_id) AS zone_id,
    LATEST_BY_OFFSET(type) AS type
FROM
    STOP_SILVER
GROUP BY
    id
EMIT CHANGES;

CREATE OR REPLACE TABLE VEHICLE_JSON
WITH (VALUE_FORMAT='JSON')
AS
SELECT
    id,
    LATEST_BY_OFFSET(event) AS event,
    LATEST_BY_OFFSET(bearing) AS bearing,
    LATEST_BY_OFFSET(current_status) AS current_status,
    LATEST_BY_OFFSET(current_stop_sequence) AS current_stop_sequence,
    LATEST_BY_OFFSET(direction_id) AS direction_id,
    LATEST_BY_OFFSET(label) AS label,
    LATEST_BY_OFFSET(latitude) AS latitude,
    LATEST_BY_OFFSET(longitude) AS longitude,
    LATEST_BY_OFFSET(speed) AS speed,
    LATEST_BY_OFFSET(updated_at) AS updated_at,
    LATEST_BY_OFFSET(self) AS self,
    LATEST_BY_OFFSET(stop_id) AS stop_id,
    LATEST_BY_OFFSET(stop_type) AS stop_type,
    LATEST_BY_OFFSET(trip_id) AS trip_id,
    LATEST_BY_OFFSET(trip_type) AS trip_type,
    LATEST_BY_OFFSET(type) AS type
FROM
    VEHICLE_SILVER
GROUP BY
    id
EMIT CHANGES;


CREATE OR REPLACE TABLE SCHEDULE_JSON
WITH (VALUE_FORMAT='JSON')
AS
SELECT
    id,
    LATEST_BY_OFFSET(event) AS event,
    LATEST_BY_OFFSET(arrival_time) AS arrival_time,
    LATEST_BY_OFFSET(departure_time) AS departure_time,
    LATEST_BY_OFFSET(direction_id) AS direction_id,
    LATEST_BY_OFFSET(drop_off_type) AS drop_off_type,
    LATEST_BY_OFFSET(pickup_type) AS pickup_type,
    LATEST_BY_OFFSET(stop_headsign) AS stop_headsign,
    LATEST_BY_OFFSET(stop_sequence) AS stop_sequence,
    LATEST_BY_OFFSET(timepoint) AS timepoint,
    LATEST_BY_OFFSET(route_id) AS route_id,
    LATEST_BY_OFFSET(route_type) AS route_type,
    LATEST_BY_OFFSET(stop_id) AS stop_id,
    LATEST_BY_OFFSET(stop_type) AS stop_type,
    LATEST_BY_OFFSET(trip_id) AS trip_id,
    LATEST_BY_OFFSET(trip_type) AS trip_type,
    LATEST_BY_OFFSET(type) AS type
FROM
    SCHEDULE_SILVER
GROUP BY
    id
EMIT CHANGES;



CREATE OR REPLACE TABLE TRIP_JSON
WITH (VALUE_FORMAT='JSON')
AS
SELECT
    id,
    LATEST_BY_OFFSET(event) AS event,
    LATEST_BY_OFFSET(bikes_allowed) AS bikes_allowed,
    LATEST_BY_OFFSET(block_id) AS block_id,
    LATEST_BY_OFFSET(direction_id) AS direction_id,
    LATEST_BY_OFFSET(headsign) AS headsign,
    LATEST_BY_OFFSET(name) AS name,
    LATEST_BY_OFFSET(wheelchair_accessible) AS wheelchair_accessible,
    LATEST_BY_OFFSET(self) AS self,
    LATEST_BY_OFFSET(shape_id) AS shape_id,
    LATEST_BY_OFFSET(shape_type) AS shape_type,
    LATEST_BY_OFFSET(service_id) AS service_id,
    LATEST_BY_OFFSET(service_type) AS service_type,
    LATEST_BY_OFFSET(route_id) AS route_id,
    LATEST_BY_OFFSET(route_type) AS route_type,
    LATEST_BY_OFFSET(route_pattern_id) AS route_pattern_id,
    LATEST_BY_OFFSET(route_pattern_type) AS route_pattern_type,
    LATEST_BY_OFFSET(type) AS type
FROM
    TRIP_SILVER
GROUP BY
    id
EMIT CHANGES;
