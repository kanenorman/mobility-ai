
-- VEHICLES
CREATE OR REPLACE STREAM VEHICLE_STREAM
(
  event STRING,
  data STRUCT<
    attributes STRUCT<
      bearing INT,
      carriages ARRAY<
        STRUCT<
          label STRING,
          occupancy_percentage INT,
          occupancy_status STRING
        >
      >,
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
)
WITH (
  KAFKA_TOPIC = 'vehicles',
  VALUE_FORMAT = 'JSON'
);


SELECT
  event,
  data->id,
  data->type,
  data->attributes->bearing,
  data->attributes->current_status,
  data->attributes->current_stop_sequence,
  data->attributes->direction_id,
  data->attributes->label,
  data->attributes->latitude,
  data->attributes->longitude,
  data->attributes->occupancy_status,
  data->attributes->speed,
  data->attributes->updated_at,
  data->relationships->route->data->id AS route_id,
  data->relationships->stop->data->id AS stop_id,
  data->relationships->trip->data->id AS trip_id
