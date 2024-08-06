import datetime
from functools import reduce

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, dense_rank, desc, lit, row_number, when
from pyspark.sql.window import Window

from spark_web_events_etl.tasks.abstract.transformation import AbstractTransformation


class CurateDataTransformation(AbstractTransformation):

    def __init__(self, execution_date: datetime.date):
        self.execution_date = execution_date

    def transform(self, df: DataFrame) -> DataFrame:
        transformations = (
            self._remove_duplicates,
            self._calculate_domain_of_interest,
            self._calculate_rank_domain_of_interest,
            self._select_final_columns,
        )

        return reduce(DataFrame.transform, transformations, df)  # type: ignore

    @staticmethod
    def _remove_duplicates(df: DataFrame) -> DataFrame:
        """Drop duplicates based on "distinct_id", keeping the first event (based on "timestamp")."""
        window_spec = Window.partitionBy(["distinct_id"]).orderBy(col("event_processed_timestamp").desc())
        df = df.withColumn("rnum", row_number().over(window_spec))
        return df.where(col("rnum") == 1).drop("rnum")

    @staticmethod
    def _calculate_domain_of_interest(df: DataFrame) -> DataFrame:
        return df.withColumn(
            "domain_of_interest",
            when(col("referring_domain") == "$direct", "direct traffic")
            .when(col("referring_domain").like("%opensea%"), "opensea")
            .when(col("referring_domain").like("%abc%"), "abc")
            .otherwise("other"),
        )

    @staticmethod
    def _calculate_rank_domain_of_interest(df: DataFrame) -> DataFrame:
        df = df.groupBy("domain_of_interest").count().withColumnRenamed("count", "unique_events")
        df = df.withColumn("rank", dense_rank().over(Window.orderBy(desc("unique_events"))))
        return df.orderBy(desc("rank"))

    def _select_final_columns(self, df: DataFrame) -> DataFrame:
        return df.select(
            "domain_of_interest",
            "unique_events",
            "rank",
            lit(int(self.execution_date.strftime("%Y%m%d"))).alias("_run_date"),
        )
