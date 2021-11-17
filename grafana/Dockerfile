FROM grafana/grafana:master

RUN grafana-cli plugins install grafana-piechart-panel
RUN grafana-cli plugins install simpod-json-datasource
RUN grafana-cli plugins install marcusolsson-json-datasource

EXPOSE 3000
