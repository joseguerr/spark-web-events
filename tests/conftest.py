from typing import Generator

import pytest as pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

from tests.utils import create_database, drop_database_cascade


@pytest.fixture(scope="session")
def spark() -> Generator:
    spark = (
        SparkSession.builder.master("local[*]")
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
        .enableHiveSupport()
        .getOrCreate()
    )
    create_database(spark, "test")
    yield spark
    drop_database_cascade(spark, "test")


@pytest.fixture(scope="session")
def schema_raw() -> StructType:
    return StructType(
        [
            StructField("_airbyte_emitted_at", StringType(), False),
            StructField("_airbyte_data", StructType([
                StructField("referring_domain", StringType(), False),
                StructField("distinct_id", StringType(), False),
                StructField("device_id", StringType(), False),
                StructField("device", StringType(), True),
                StructField("current_url", StringType(), False),
                StructField("processed_time", StringType(), False)
        ]), False)
    ])


@pytest.fixture(scope="session")
def schema_standardised() -> StructType:
    return StructType([
        StructField("distinct_id", StringType(), False),
        StructField("device_id", StringType(), False),
        StructField("referring_domain", StringType(), False),
        StructField("current_url", StringType(), False),
        StructField("device", StringType(), True),
        StructField("event_processed_timestamp", LongType(), False),
        StructField("airbyte_emitted_at_timestamp", LongType(), False),
        StructField("_run_date", IntegerType(), False)
    ])


@pytest.fixture(scope="session")
def schema_curated() -> StructType:
    return StructType(
        [
            StructField("domain_of_interest", StringType(), False),
            StructField("unique_events", LongType(), False),
            StructField("rank", IntegerType(), False),
            StructField("_run_date", IntegerType(), False),
        ]
    )
