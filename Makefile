.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: setup
setup: # Set up local virtual env for development.
	pip install --upgrade pip setuptools wheel poetry
	poetry config virtualenvs.in-project true --local
	poetry install

.PHONY: lint
lint: # Run code linter tools.
	poetry run pre-commit run --all-files

.PHONY: test
test: # Run unit and integration tests.
	poetry run pytest --cov=spark_web_events_etl --cov-report=xml --cov-report=term-missing -vvvv --showlocals --disable-warnings tests

.PHONY: build
build: # Build and package the application and its dependencies to be used through spark-submit.
	poetry build
	poetry run pip install dist/*.whl -t libs
	mkdir deps
	cp spark_web_events_etl/main.py app_config.yaml spark_web_events_etl/tasks/*/dq_checks_*.yaml deps
	poetry run python -m zipfile -c deps/libs.zip libs/*

.PHONY: run-local
run-local: # Run a task locally (example: make run-local task=standardise execution-date=2023-04-12).
	poetry run spark-submit \
	--master local[*] \
	--packages=io.delta:delta-spark_2.12:3.2.0 \
	--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
	--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
	spark_web_events_etl/main.py \
	--task ${task} \
	--execution-date ${execution-date} \
	--config-file-path app_config.yaml

.PHONY: clean
clean: # Clean auxiliary files.
	rm -rf deps/ dist/ libs/ .pytest_cache .mypy_cache spark_web_events_etl.egg-info *.xml .coverage* derby.log metastore_db spark-warehouse
