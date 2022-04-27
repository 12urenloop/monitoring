FROM grafana/grafana:8.5.0

RUN grafana-cli plugins install grafana-piechart-panel
RUN grafana-cli plugins install simpod-json-datasource
RUN grafana-cli plugins install marcusolsson-json-datasource
RUN grafana-cli plugins install yesoreyeram-infinity-datasource


EXPOSE 3000
