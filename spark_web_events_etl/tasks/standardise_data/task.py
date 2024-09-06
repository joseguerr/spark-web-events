from pyspark.sql import DataFrame
from pyspark.sql.types import StringType, StructField, StructType

from spark_web_events_etl.tasks.abstract.task import AbstractTask
from spark_web_events_etl.tasks.standardise_data.transformation import \
    StandardiseDataTransformation


class StandardiseDataTask(AbstractTask):
    @property
    def _input_path(self) -> str:
        execution_date_str = self.execution_date.strftime("%Y/%m/%d")
        return f"{self.config_manager.get('data.raw.location')}/{execution_date_str}"

    @property
    def _output_table(self) -> str:
        return self.config_manager.get("data.standardised.table")

    @property
    def _dq_checks_config_file(self) -> str:
        return self.config_manager.get("data.standardised.dq_checks_file")

    @property
    def _get_schema(self) -> StructType:
        # Define low-level schema
        airbyte_data_schema = StructType(
            [
                StructField("distinct_id", StringType(), True),
                StructField("device_id", StringType(), True),
                StructField("referring_domain", StringType(), True),
                StructField("current_url", StringType(), True),
                StructField("device", StringType(), True),
                StructField("processed_time", StringType(), True),
            ]
        )

        # Define top-level schema
        self.schema = StructType(
            [
                StructField("_airbyte_emitted_at", StringType(), True),
                StructField("_airbyte_data", airbyte_data_schema, True),
            ]
        )
        return self.schema

    def _input(self) -> DataFrame:
        self.logger.info(f"Reading raw data from {self._input_path}.")
        return (
            self.spark.read.format("json")
            .schema(self._get_schema)
            .load(path=self._input_path)
        )

    def _transform(self, df: DataFrame) -> DataFrame:
        return StandardiseDataTransformation(self.execution_date).transform(df)
