from datetime import date

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

from spark_web_events_etl.tasks.curate_data.transformation import \
    CurateDataTransformation
from tests.unit.tasks.curate_data.fixtures.data import (
    TEST_TRANSFORM_INPUT, TEST_TRANSFORM_OUTPUT_EXPECTED)
from tests.utils import assert_data_frames_equal


def test_transform(
    spark: SparkSession, schema_standardised: StructType, schema_curated: StructType
) -> None:
    # GIVEN
    transformation = CurateDataTransformation(execution_date=date(2023, 4, 12))
    df_input = spark.createDataFrame(
        TEST_TRANSFORM_INPUT,
        schema=schema_standardised,
    )
    df_expected = spark.createDataFrame(
        TEST_TRANSFORM_OUTPUT_EXPECTED,
        schema=schema_curated,
    )

    # WHEN
    df_transformed = transformation.transform(df_input)

    # THEN
    assert_data_frames_equal(df_transformed, df_expected)
