import datetime
from functools import reduce

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit
from pyspark.sql.types import LongType

from spark_web_events_etl.tasks.abstract.transformation import \
    AbstractTransformation


class StandardiseDataTransformation(AbstractTransformation):
    def __init__(self, execution_date: datetime.date):
        self.execution_date = execution_date

    def transform(self, df: DataFrame) -> DataFrame:
        transformations = (
            self._normalise_columns,
            self._select_final_columns,
        )

        return reduce(DataFrame.transform, transformations, df)

    @staticmethod
    def _normalise_columns(df: DataFrame) -> DataFrame:
        return (
            df.withColumn("distinct_id", col("_airbyte_data.distinct_id"))
            .withColumn("device_id", col("_airbyte_data.device_id"))
            .withColumn("referring_domain", col("_airbyte_data.referring_domain"))
            .withColumn("current_url", col("_airbyte_data.current_url"))
            .withColumn("device", col("_airbyte_data.device"))
            .withColumn(
                "event_processed_timestamp",
                col("_airbyte_data.processed_time").cast(LongType()),
            )
            .withColumn(
                "airbyte_emitted_at_timestamp",
                col("_airbyte_emitted_at").cast(LongType()),
            )
        )

    def _select_final_columns(self, df: DataFrame) -> DataFrame:
        return df.select(
            "distinct_id",
            "device_id",
            "referring_domain",
            "current_url",
            "device",
            "event_processed_timestamp",
            "airbyte_emitted_at_timestamp",
            lit(int(self.execution_date.strftime("%Y%m%d"))).alias("_run_date"),
        )
