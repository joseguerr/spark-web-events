import datetime
from abc import ABC, abstractmethod
from logging import Logger
from typing import List

from pyspark.sql import Catalog, DataFrame, SparkSession
from soda.scan import Scan

from spark_web_events_etl.config_manager import ConfigManager


class AbstractTask(ABC):
    """
    Base class to read a dataset, transform it, and save it to a table.
    """

    def __init__(
        self,
        spark: SparkSession,
        logger: Logger,
        execution_date: datetime.date,
        config_manager: ConfigManager,
    ):
        self.spark = spark
        self.execution_date = execution_date
        self.config_manager = config_manager
        self.logger = logger

    def run(self) -> None:
        df = self._input()
        df_transformed = self._transform(df)
        self._output(df_transformed)
        self._run_data_quality_checks()

    @abstractmethod
    def _input(self) -> DataFrame:
        raise NotImplementedError

    @abstractmethod
    def _transform(self, df: DataFrame) -> DataFrame:
        raise NotImplementedError

    def _output(self, df: DataFrame) -> None:
        self.logger.info(f"Saving to table {self._output_table}.")

        if self._table_exists(self._output_table):
            self.logger.info("Table exists, inserting.")
            df.write.mode("overwrite").insertInto(self._output_table)
        else:
            self.logger.info("Table does not exist, creating and saving.")
            partition_cols = [self._partition_column_run_day] + self._partition_columns_extra
            df.write.mode("overwrite").partitionBy(partition_cols).format("delta").saveAsTable(self._output_table)

    def _run_data_quality_checks(self) -> None:
        self.logger.info(f"Running Data Quality checks for table {self._output_table}.")
        scan = Scan()

        scan.set_data_source_name("spark_df")
        scan.add_spark_session(self.spark)
        scan.add_variables(
            {
                "table": self._output_table,
                "run_date": self.execution_date.strftime("%Y%m%d"),
            }
        )
        scan.add_sodacl_yaml_file(self._dq_checks_config_file)

        scan.execute()

        self.logger.info(scan.get_scan_results())
        scan.assert_no_error_logs()
        scan.assert_no_checks_fail()

    @property
    @abstractmethod
    def _output_table(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def _dq_checks_config_file(self) -> str:
        raise NotImplementedError

    @property
    def _partition_column_run_day(self) -> str:
        return "_run_date"

    @property
    def _partition_columns_extra(self) -> List[str]:
        return []

    def _table_exists(self, table: str) -> bool:
        return Catalog(self.spark).tableExists(table)
