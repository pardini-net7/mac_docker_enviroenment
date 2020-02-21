#!/usr/bin/env bash
export ROOT_PATH="/Users/max2thousand/mac_docker_enviroenment"
PW=$1
#Reboot NFS
echo $PW | sudo nfsd restart
#RESTART ALL
cd $ROOT_PATH/solr7 && docker-compose down --rmi=local && docker-compose up -d;
cd $ROOT_PATH/postgres && docker-compose down --rmi=local && docker-compose up -d;
cd $ROOT_PATH/mariadb && docker-compose down --rmi=local && docker-compose up -d;
cd $ROOT_PATH/elasticsearch && docker-compose down --rmi=local && docker-compose up -d;
cd $ROOT_PATH/phpfpm7.2 && docker-compose down --rmi=local && docker-compose up -d;
cd $ROOT_PATH/nginx && docker-compose down --rmi=local && docker-compose up -d;
cd $ROOT_PATH/phpmyadmin && docker-compose down --rmi=local && docker-compose up -d;
#cd $ROOT_PATH/docker-geoserver && docker-compose down --rmi=local && docker-compose up -d;