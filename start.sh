#!/bin/bash

# Getting IPs
source ${1:-config_prod.env}

# Setting Grafana password
sed -i "s/MONITORING_MASTER_PASSWORD/${MONITORING_MASTER_PASSWORD}/" grafana/config.monitoring

# Setting IPs in different files
sed -i "s/IP_AND_PORT_RONNY01/${RONNY01_IP}:${RONNY01_PORT}/" prometheus/http_hosts.yml
sed -i "s/IP_AND_PORT_RONNY02/${RONNY02_IP}:${RONNY02_PORT}/" prometheus/http_hosts.yml
sed -i "s/IP_AND_PORT_RONNY03/${RONNY03_IP}:${RONNY03_PORT}/" prometheus/http_hosts.yml
sed -i "s/IP_AND_PORT_RONNY04/${RONNY04_IP}:${RONNY04_PORT}/" prometheus/http_hosts.yml
sed -i "s/IP_AND_PORT_RONNY05/${RONNY05_IP}:${RONNY05_PORT}/" prometheus/http_hosts.yml
sed -i "s/IP_AND_PORT_RONNY06/${RONNY06_IP}:${RONNY06_PORT}/" prometheus/http_hosts.yml
sed -i "s/IP_AND_PORT_RONNY07/${RONNY07_IP}:${RONNY07_PORT}/" prometheus/http_hosts.yml
sed -i "s/IP_AND_PORT_TELRAAM/${TELRAAM_IP}:${TELRAAM_PORT}/" prometheus/http_hosts.yml

sed -i "s/IP_RONNY01/${RONNY01_IP}/" prometheus/ping_hosts.yml
sed -i "s/IP_RONNY02/${RONNY02_IP}/" prometheus/ping_hosts.yml
sed -i "s/IP_RONNY03/${RONNY03_IP}/" prometheus/ping_hosts.yml
sed -i "s/IP_RONNY04/${RONNY04_IP}/" prometheus/ping_hosts.yml
sed -i "s/IP_RONNY05/${RONNY05_IP}/" prometheus/ping_hosts.yml
sed -i "s/IP_RONNY06/${RONNY06_IP}/" prometheus/ping_hosts.yml
sed -i "s/IP_RONNY07/${RONNY07_IP}/" prometheus/ping_hosts.yml
sed -i "s/IP_CLIENT1/${CLIENT1_IP}/" prometheus/ping_hosts.yml
sed -i "s/IP_CLIENT2/${CLIENT2_IP}/" prometheus/ping_hosts.yml

sed -i "s/IP_TELRAAM/${TELRAAM_IP}/" prometheus/prometheus.yml
sed -i "s/IP_RONNY01/${RONNY01_IP}/" prometheus/prometheus.yml
sed -i "s/IP_RONNY02/${RONNY02_IP}/" prometheus/prometheus.yml
sed -i "s/IP_RONNY03/${RONNY03_IP}/" prometheus/prometheus.yml
sed -i "s/IP_RONNY04/${RONNY04_IP}/" prometheus/prometheus.yml
sed -i "s/IP_RONNY05/${RONNY05_IP}/" prometheus/prometheus.yml
sed -i "s/IP_RONNY06/${RONNY06_IP}/" prometheus/prometheus.yml
sed -i "s/IP_RONNY07/${RONNY07_IP}/" prometheus/prometheus.yml
sed -i "s/IP_CLIENT1/${CLIENT1_IP}/" prometheus/prometheus.yml
sed -i "s/IP_CLIENT2/${CLIENT2_IP}/" prometheus/prometheus.yml

sed -i "s/IP_AND_PORT_MANUALCOUNT/${MANUALCOUNT_IP}:${MANUALCOUNT_PORT}/" grafana/provisioning/datasources/datasource.yml
sed -i "s/IP_AND_PORT_TELRAAM/${TELRAAM_IP}:${TELRAAM_PORT}/" grafana/provisioning/datasources/datasource.yml

sed -i "s/IP_AND_PORT_MANUALCOUNT/${MANUALCOUNT_IP}:${MANUALCOUNT_PORT}/" timesync/config.py
sed -i "s/IP_AND_PORT_TELRAAM/${TELRAAM_IP}:${TELRAAM_PORT}/" timesync/config.py

# Starting monitoring
docker-compose up
