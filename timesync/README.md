# Timesync

A simple flask server that collects the value of the current clocks of the Stations and other important running servers. It them compares them and provides a simple overview of their offset.

## Development

```sh
make dev
```

## Production

Using gunicorn with gevent.

```sh
make prod
```
