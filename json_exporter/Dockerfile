FROM prometheuscommunity/json-exporter:v0.7.0

COPY json.yml       /etc/json_exporter/config.yml

EXPOSE      9115
ENTRYPOINT  [ "/bin/json_exporter" ]
CMD         [ "--config.file=/etc/json_exporter/config.yml" ]
