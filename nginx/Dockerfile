FROM nginx:alpine

WORKDIR /var/www/html
ENV USER=wodby
ENV UID=501
ENV GID=dialout

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup "$GID" \
    --no-create-home \
    --uid "$UID" \
    "$USER"


RUN rm -f /etc/nginx/conf.d/default.conf
COPY drupal.conf /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/nginx.conf