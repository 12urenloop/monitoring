# Monitoring

A monitoring stack that makes use of grafana for visualizations.

It also contains prometheus as option to collect metrics and serve them to grafana.
It should be invested if this is usefull and if we don't want to use an http api instead.

## Features

- Status overview of the running services and devices. Pings devices and makes http requests to web servers. Also shows a map of the stations.
- Data overview of telraam. Just a page with tables and a simple lap overview
- WIP: Lap insight page. 
  - See laps over time. 
  - Detect sudden lap duration differences
  - ...

## Requirements

- docker-compose

## Usage

```
docker-compose up
```

Go to [localhost:3000](http://localhost:3000) to see the grafana dashboard.
The preset credentials are username `admin` and password `foobar`.


## Resources


https://medium.com/the-telegraph-engineering/how-prometheus-and-the-blackbox-exporter-makes-monitoring-microservice-endpoints-easy-and-free-of-a986078912ee
