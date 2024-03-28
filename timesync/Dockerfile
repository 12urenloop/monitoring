FROM debian:latest

RUN apt-get update && \
	apt-get install -yqq --no-install-recommends python3-pip python3-venv build-essential

WORKDIR /app
RUN python3 -m venv /app/venv
ADD requirements.txt requirements.prod.txt ./
RUN /app/venv/bin/pip install -r requirements.txt

ADD . .

# source: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
# ENTRYPOINT ["make", "prod"]
CMD . /app/venv/bin/activate && exec make prod
