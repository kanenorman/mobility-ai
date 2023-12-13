# TODO: SETUP SECRETS TO PROTECT LOG OUTPUTS.
# FOR NOW REDIRECT OUTPUT TO /dev/null

# VEHICLE TABLE
curl -s -X PUT -H "Content-Type: application/json" http://connect:8083/connectors/postgres-vehicle-sink/config -d '{
    "name": "postgres-vehicle-sink",
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "transforms": "RemaneField",
    "topics": "VEHICLE_GOLD",
    "transforms.RemaneField.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
    "transforms.RemaneField.renames": "EVENT:event, BEARING:bearing, CURRENT_STATUS:current_status, CURRENT_STOP_SEQUENCE:current_stop_sequence, DIRECTION_ID:direction_id, LABEL:label, LATITUDE:latitude, LONGITUDE:longitude, SPEED:speed, UPDATED_AT:updated_at, SELF:self, STOP_ID:stop_id, STOP_TYPE:stop_type, TRIP_ID:trip_id, TRIP_TYPE:trip_type, TYPE:type, ID:id",
    "connection.url": "jdbc:postgresql://flask_database:5432/mbta?user='${POSTGRES_USER}'&password='${POSTGRES_PASSWORD}'",
    "connection.user": "'${POSTGRES_USER}'",
    "connection.password": "'${POSTGRES_PASSWORD}'",
    "dialect.name": "PostgreSqlDatabaseDialect",
    "insert.mode": "upsert",
    "table.name.format": "vehicle",
    "pk.mode": "record_key",
    "pk.fields": "id"
}'  >/dev/null 2>&1

# STOP TABLE
curl -s -X PUT -H "Content-Type: application/json" http://connect:8083/connectors/postgres-stop-sink/config -d '{
    "name": "postgres-stop-sink",
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "transforms": "RemaneField",
    "topics": "STOP_GOLD",
    "transforms.RemaneField.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
    "transforms.RemaneField.renames": "EVENT:event, ADDRESS:address, AT_STREET:at_street, DESCRIPTION:description, LATITUDE:latitude, LOCATION_TYPE:location_type, LONGITUDE:longitude, MUNICIPALITY:municipality, NAME:name, ON_STREET:on_street, PLATFORM_CODE:platform_code, PLATFORM_NAME:platform_name, VEHICLE_TYPE:vehicle_type, WHEELCHAIR_BOARDING:wheelchair_boarding, SELF:self, FACILITIES_SELF:facilities_self, PARENT_STATION_ID:parent_station_id, PARENT_STATION_TYPE:parent_station_type, ZONE_ID:zone_id, TYPE:type, ID:id",
    "connection.url": "jdbc:postgresql://flask_database:5432/mbta?user='${POSTGRES_USER}'&password='${POSTGRES_PASSWORD}'",
    "connection.user": "'${POSTGRES_USER}'",
    "connection.password": "'${POSTGRES_PASSWORD}'",
    "dialect.name": "PostgreSqlDatabaseDialect",
    "insert.mode": "upsert",
    "table.name.format": "stop",
    "pk.mode": "record_key",
    "pk.fields": "id"
}'  >/dev/null 2>&1

# SCHEDULE TABLE
curl -s -X PUT -H "Content-Type: application/json" http://connect:8083/connectors/postgres-schedule-sink/config -d '{
    "name": "postgres-schedule-sink",
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "transforms": "RemaneField",
    "topics": "SCHEDULE_GOLD",
    "transforms.RemaneField.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
    "transforms.RemaneField.renames": "EVENT:event, ARRIVAL_TIME:arrival_time, DEPARTURE_TIME:departure_time, DIRECTION_ID:direction_id, DROP_OFF_TYPE:drop_off_type, PICKUP_TYPE:pickup_type, STOP_HEADSIGN:stop_headsign, STOP_SEQUENCE:stop_sequence, TIMEPOINT:timepoint, ROUTE_ID:route_id, ROUTE_TYPE:route_type, STOP_ID:stop_id, STOP_TYPE:stop_type, TRIP_ID:trip_id, TRIP_TYPE:trip_type, TYPE:type, ID:id",
    "connection.url": "jdbc:postgresql://flask_database:5432/mbta?user='${POSTGRES_USER}'&password='${POSTGRES_PASSWORD}'",
    "connection.user": "'${POSTGRES_USER}'",
    "connection.password": "'${POSTGRES_PASSWORD}'",
    "dialect.name": "PostgreSqlDatabaseDialect",
    "insert.mode": "upsert",
    "table.name.format": "schedule",
    "pk.mode": "record_key",
    "pk.fields": "id"
}'  >/dev/null 2>&1

# TRIP TABLE
curl -s -X PUT -H "Content-Type: application/json" http://connect:8083/connectors/postgres-trip-sink/config -d '{
    "name": "postgres-trip-sink",
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "transforms": "RemaneField",
    "topics": "TRIP_GOLD",
    "transforms.RemaneField.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
    "transforms.RemaneField.renames": "EVENT:event, BIKES_ALLOWED:bikes_allowed, BLOCK_ID:block_id, DIRECTION_ID:direction_id, HEADSIGN:headsign, NAME:name, WHEELCHAIR_ACCESSIBLE:wheelchair_accessible, SELF:self, SHAPE_ID:shape_id, SHAPE_TYPE:shape_type, SERVICE_ID:service_id, SERVICE_TYPE:service_type, ROUTE_ID:route_id, ROUTE_TYPE:route_type, ROUTE_PATTERN_ID:route_pattern_id, ROUTE_PATTERN_TYPE:route_pattern_type, TYPE:type, ID:id",
    "connection.url": "jdbc:postgresql://flask_database:5432/mbta?user='${POSTGRES_USER}'&password='${POSTGRES_PASSWORD}'",
    "connection.user": "'${POSTGRES_USER}'",
    "connection.password": "'${POSTGRES_PASSWORD}'",
    "dialect.name": "PostgreSqlDatabaseDialect",
    "insert.mode": "upsert",
    "table.name.format": "trip",
    "pk.mode": "record_key",
    "pk.fields": "id"
}'  >/dev/null 2>&1

# ROUTE TABLE
curl -s -X PUT -H "Content-Type: application/json" http://connect:8083/connectors/postgres-route-sink/config -d '{
    "name": "postgres-route-sink",
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "transforms": "RemaneField",
    "topics": "ROUTE_GOLD",
    "transforms.RemaneField.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
    "transforms.RemaneField.renames": "EVENT:event, COLOR:color, DESCRIPTION:description, DIRECTION_DESTINATIONS:direction_destinations, DIRECTION_NAMES:direction_names, FARE_CLASS:fare_class, LONG_NAME:long_name, SHORT_NAME:short_name, SHORT_ORDER:short_order, TEXT_COLOR:text_color, TYPE:type, SELF:self, LINE_ID:line_id, LINE_TYPE:line_type, ID:id",
    "connection.url": "jdbc:postgresql://flask_database:5432/mbta?user='${POSTGRES_USER}'&password='${POSTGRES_PASSWORD}'",
    "connection.user": "'${POSTGRES_USER}'",
    "connection.password": "'${POSTGRES_PASSWORD}'",
    "dialect.name": "PostgreSqlDatabaseDialect",
    "insert.mode": "upsert",
    "table.name.format": "route",
    "pk.mode": "record_key",
    "pk.fields": "id"
}'  >/dev/null 2>&1
