#!/bin/bash

# Getting IPs
set -a # Set the 'allexport' option to make sure all variables that are sourced are exported again.
. ${1:-config_prod.env}

export IP_PORT_RONNY01="${RONNY01_IP}:${RONNY01_PORT}"
export IP_PORT_RONNY02="${RONNY02_IP}:${RONNY02_PORT}"
export IP_PORT_RONNY03="${RONNY03_IP}:${RONNY03_PORT}"
export IP_PORT_RONNY04="${RONNY04_IP}:${RONNY04_PORT}"
export IP_PORT_RONNY05="${RONNY05_IP}:${RONNY05_PORT}"
export IP_PORT_RONNY06="${RONNY06_IP}:${RONNY06_PORT}"
export IP_PORT_RONNY07="${RONNY07_IP}:${RONNY07_PORT}"
export IP_PORT_TELRAAM="${TELRAAM_IP}:${TELRAAM_PORT}"
export IP_PORT_MANUALCOUNT="${MANUALCOUNT_IP}:${MANUALCOUNT_PORT}"

envsubst < prometheus/http_hosts.template.yml \
         > prometheus/http_hosts.yml
envsubst < prometheus/ping_hosts.template.yml \
         > prometheus/ping_hosts.yml
envsubst < prometheus/prometheus.template.yml \
         > prometheus/prometheus.yml

mkdir -p grafana/provisioning/datasources
envsubst < grafana/datasource.template.yml \
         > grafana/provisioning/datasources/datasource.yml
envsubst < grafana/config.template.monitoring \
         > grafana/config.monitoring

envsubst < timesync/config.template.py \
         > timesync/config.py

# Starting monitoring
docker-compose up --build -d
