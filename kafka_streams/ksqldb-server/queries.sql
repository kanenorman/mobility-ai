SET 'auto.offset.reset'='earliest';

CREATE OR REPLACE STREAM VEHICLE_STREAM (
  event STRING,
  data STRUCT<
    attributes STRUCT<
      bearing INT,
      carriages ARRAY<STRUCT<
        label STRING,
        occupancy_percentage INT,
        occupancy_status STRING
      >>,
      current_status STRING,
      current_stop_sequence INT,
      direction_id INT,
      label STRING,
      latitude DOUBLE,
      longitude DOUBLE,
      occupancy_status STRING,
      speed INT,
      updated_at STRING
    >,
    id STRING,
    links STRUCT<
      self STRING
    >,
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
  KAFKA_TOPIC = 'vehicle-topic',
  VALUE_FORMAT = 'JSON'
);

CREATE OR REPLACE STREAM TRIP_STREAM (
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

CREATE OR REPLACE STREAM STOP_STREAM (
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

CREATE OR REPLACE STREAM SCHEDULE_STREAM (
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

CREATE OR REPLACE STREAM ROUTE_STREAM (
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

CREATE OR REPLACE STREAM SHAPE_STREAM (
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
