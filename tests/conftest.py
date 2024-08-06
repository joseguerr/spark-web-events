from typing import Generator

import pytest as pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    ArrayType,
    BooleanType,
    FloatType,
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
            StructField("_airbyte_emitted_at", StringType()),
            StructField(
                "_airbyte_data",
                ArrayType(
                    StructType(
                        [
                            StructField("referring_domain", StringType()),
                            StructField("distinct_id", StringType()),
                            StructField("device_id", StringType()),
                            StructField("device", StringType(), nullable=True),
                            StructField("current_url", StringType()),
                            StructField("processed_time", StringType()),
                        ]
                    )
                ),
                nullable=False,
            ),
        ]
    )


@pytest.fixture(scope="session")
def schema_standardised() -> StructType:
    return StructType(
        [
            StructField("distinct_id", StringType()),
            StructField("device_id", StringType()),
            StructField("referring_domain", StringType()),
            StructField("current_url", StringType()),
            StructField("device", StringType()),
            StructField("event_processed_timestamp", LongType()),
            StructField("airbyte_emitted_at_timestamp", LongType()),
            StructField("_run_date", IntegerType()),
        ]
    )


@pytest.fixture(scope="session")
def schema_curated() -> StructType:
    return StructType(
        [
            StructField("domain_of_interest", StringType()),
            StructField("unique_events", LongType()),
            StructField("rank", IntegerType()),
            StructField("_run_date", IntegerType()),
        ]
    )
