# Monitoring

A monitoring stack that makes use of [Grafana](https://grafana.com/) for visualizations.

It also contains [Prometheus](https://prometheus.io/) to collect metrics and serve them to Grafana. Grafana uses both Prometheus en the Telraam HTTP-API to collect and show data. Data transformations are limited in Grafana, because of this the `timesync` folder contains code that collects, transforms and exposes data and metrics in a simple flask webserver to be used by Grafana.

Use it together with the [mityri](https://github.com/12urenloop/mityri) mock tools to instantly observe stats and metrics of a near real setup.

Use it together with the [banshee](https://github.com/12urenloop/banshee) alert watcher to be sure you don't miss the prometheus alerts.

## Features

- **Status overview**: Status of the running services and devices. Pings devices and makes http requests to web servers. Shows a map of the stations. Tracks the time sync between our services.
  - Baton battery percentage
  - Baton battery last seen time
  - Baton restarted status: if a baton uptime changes more then 3s between detections it is seen as *restarted*. This means something is going wrong and you want to check the baton for malfuctioning parts. If everything is fine you can set this restart status as fine by posting to the endpoint `/reset_rebooted/<mac>`. Restarting the timesync server re-mark this baton as restarted.
- **Data overview** of telraam. Just a page with tables and a simple lap overview
- WIP: Lap insight page. 
  - See laps over time. 
  - Detect sudden lap duration differences
- **Postgres overview**: Monitors the postgres behavior using a postgres exporter for prometheus: https://github.com/prometheus-community/postgres_exporter

## Requirements

- docker-compose

## Usage

Configure the configuration of the Stations and Telraam in the `prometheus` folder.

Configure the correct ip adressess in the datasources files in the `grafana` folder.

Configure the correct ip adresses in the config file in the `timesync` folder.


```
docker-compose up
```

Go to [localhost:3000](http://localhost:3000) to see the grafana dashboard.
The preset credentials are username `admin` and password `foobar`.


## Resources


https://medium.com/the-telegraph-engineering/how-prometheus-and-the-blackbox-exporter-makes-monitoring-microservice-endpoints-easy-and-free-of-a986078912ee
