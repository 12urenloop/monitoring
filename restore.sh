#!/bin/bash

read -p "Warning: this will reset changes to some files [y/n]: " yn
[[ "${yn}" == [Yy]* ]] || exit 1

git restore grafana/config.monitoring
git restore prometheus/http_hosts.yml
git restore prometheus/ping_hosts.yml
git restore prometheus/prometheus.yml
git restore grafana/provisioning/datasources/datasource.yml
git restore timesync/config.py
