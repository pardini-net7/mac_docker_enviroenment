# MB net7 Postgres with Postgis extension

#   Postgres version details
ARG PSQL_VERSION=11

#   New database details
ARG NEW_DB_NAME=ras
ARG NEW_DB_USER=ras
ARG NEW_DB_USER_PASSWORD=ras

#   Select image from docker hub
FROM postgres:${PSQL_VERSION}

#   Do everything as root
USER root

#   Add some files to postgres_postgis custom docker image
ADD initdb.sh /root/initdb.sh
ADD bashrc /root/.bashrc

#   Install postgis and vim, clear aptitude cache and set initial script as executable
RUN build_packages="vim postgis" \
    && apt-get update && apt-get install -y $build_packages \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && chmod u+x /root/initdb.sh

