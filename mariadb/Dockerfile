#MARIADB image
FROM mariadb
RUN apt-get update && apt-get install -y \
        vim \
        mysql-client
#Copy my.cnf with all the settings
ADD ./config/my.cnf /etc/mysql/my.cnf
EXPOSE 3306


