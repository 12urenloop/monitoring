FROM grafana/grafana:9.3.6


RUN grafana-cli plugins install grafana-piechart-panel
RUN grafana-cli plugins install simpod-json-datasource
RUN grafana-cli plugins install marcusolsson-json-datasource
RUN grafana-cli plugins install grafana-clock-panel


EXPOSE 3000
