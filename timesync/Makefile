.PHONY: init base-deps dev-deps prod-deps dev prod

base-deps:
	pip install -r requirements.txt

dev-deps: base-deps

prod-deps: base-deps
	pip install -r requirements.prod.txt


dev: dev-deps
	python3 timesync.py
	
prod: prod-deps
	python3 -m gunicorn -k gevent -b 0.0.0.0:3030 "wsgi:app"
