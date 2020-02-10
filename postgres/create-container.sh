#where store postgresql log files
#mkdir -p /docker-data/log/postgresql/
#where store postgresql backups
#mkdir -p /docker-data/backups/postgresql
#where store postgresql db data
#mkdir -p /docker-data/data/postgresql


#chown -R 999:999 /docker-data/log/postgresql/
#chown -R 999:999 /docker-data/postgresql/data
#chown -R 999:999 /docker-data/postgresql/configuration

docker-compose up -d
