BERYL_TOKENS ?=

all: run

init:
	poetry env use 3.10
	poetry install
	touch Bot/.env
	echo 'Beryl_Keys="$(BERYL_TOKENS)"' >> Bot/.env

run:
	poetry run python Bot/beryl.py
