#!/bin/bash
set -e

db_name=$1
db_user=$2
db_user_password=$3

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $db_user WITH PASSWORD '$db_user_password';
    CREATE DATABASE $db_name;
    GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;
    CREATE EXTENSION postgis;
EOSQL
