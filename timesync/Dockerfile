FROM debian:latest

RUN apt-get update && \
	apt-get install -yqq --no-install-recommends python3-pip build-essential

WORKDIR /app
ADD requirements.txt requirements.prod.txt ./
RUN pip install -r requirements.txt

ADD . .

ENTRYPOINT ["make", "prod"]
