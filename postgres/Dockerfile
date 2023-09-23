FROM postgres:15

RUN apt-get update && apt-get  install -y postgresql-15-postgis-3  

COPY postgres/db/init.sql /docker-entrypoint-initdb.d/

