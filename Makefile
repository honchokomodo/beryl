BERYL_TOKENS ?=
PM2_PUBLIC_KEY_INGEST ?=
PM2_SECRET_KEY_INGEST ?=
DOCKER_TAG_VERSION ?=

all: run

init:
	poetry env use 3.10
	poetry install
	touch Bot/.env
	echo 'Beryl_Keys="$(BERYL_TOKENS)"' >> Bot/.env

run:
	poetry run python Bot/beryl.py

deploy:
	sudo docker build -t no767/beryl:$(DOCKER_TAG_VERSION) --build-arg PM2_PUBLIC_KEY_INGEST=$(PM2_PUBLIC_KEY_INGEST) --build-arg PM2_SECRET_KEY_INGEST=$(PM2_SECRET_KEY_INGEST) -f ./Dockerfile .
