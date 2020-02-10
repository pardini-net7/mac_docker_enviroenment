FROM wodby/php:7.3-dev-macos
USER root

WORKDIR /var/www/html
COPY www.conf /usr/local/etc/php-fpm.d/www.conf


#INSTALL PHP-GEOS
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && apk --no-cache --update upgrade musl && apk update && apk add --update --no-cache gcc \
        g++ \
        autoconf
COPY geos-3.8.0 /var/www/conf/geos-3.8.0
RUN cd /var/www/conf/geos-3.8.0 && chmod +x configure && chmod -R 777 . && ./configure && make && make install
RUN cd /var/www/conf && git clone https://git.osgeo.org/gitea/geos/php-geos.git
RUN cd /var/www/conf/php-geos && chmod -R 777 . && ./autogen.sh && chmod -R 777 . && ./configure && make && make install
RUN docker-php-ext-enable geos

RUN apk add --no-cache --update --virtual buildDeps autoconf && apk del buildDeps
