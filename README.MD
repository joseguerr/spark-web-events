# Spark ETL to ingest Web Events
Spark data pipeline that ingests and transforms airbyte events data.

## Data Architecture
Implemented Data Lakehouse architecture with the following layers:
- `Raw`: Contains raw data files directly ingested from an event stream, e.g. Kafka. This data should generally not be accessible.
- `Standardised`: Contains standardized data (catalogued tables) based on the raw data with basic cleaning transformations applied -> PII masking, flatten nested columns and basic data quality checks.
- `Curated`: Contains transformed data (catalogued tables) according to business and data quality rules.

[Delta](https://delta.io/) is used as the table format.

## Data pipeline design
The data pipeline consists of the following tasks:
 - Standardise task: Flattens data and applies basic data quality checks. This may be beneficial for many teams. 
 - Curate task: consumes the dataset from `Standardised`, performs transformations and business logic, and persists into `Curated`.

The datasets are initially partitioned by execution date (with the option to add more partitioning columns).

Each task runs Data Quality checks on the output dataset just after writing. Data Quality checks are defined using [Soda](https://docs.soda.io/soda-core/overview-main.html).

## Configuration management
Configuration is defined in [app_config.yaml](app_config.yaml) and managed by the [ConfigManager](spark_web_events_etl/config_manager.py) class, which is a wrapper around [Dynaconf](https://www.dynaconf.com/).

## Packaging and dependency management
[Poetry](https://python-poetry.org/) is used for Python packaging and dependency management.

## Pre-requisites
- OpenJDK@17
- Scala@2.12
- Spark@3.5.0
- Python@3.11

## Execution instructions
The repo includes a `Makefile`. Please run `make help` to see usage.

```bash
make setup
```
```bash
make build
```
Raw data is currently under data-lake-raw-dev/airbyte/2023/04/12 (feel free to choose other data). To obtain the results run:
```bash
make run-local task=standardise execution-date=2023-04-12
```
```bash
make run-local task=curate execution-date=2023-04-12
```
