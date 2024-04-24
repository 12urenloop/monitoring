FROM prom/snmp-exporter:v0.25.0

COPY ./snmp.yml /etc/snmp_exporter/snmp.yml

EXPOSE      9116
ENTRYPOINT  [ "/bin/snmp_exporter" ]
CMD         [ "--config.file=/etc/snmp_exporter/snmp.yml" ]
