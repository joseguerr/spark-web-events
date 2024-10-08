import argparse
import datetime
import pathlib

from pyspark.sql import SparkSession

from spark_web_events_etl.config_manager import ConfigManager
from spark_web_events_etl.tasks.task_runner import TaskRunner


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("--task", type=str, required=True, choices=["standardise", "curate"])
    parser.add_argument("--execution-date", type=datetime.date.fromisoformat, required=True)
    parser.add_argument("--config-file-path", type=pathlib.Path, required=True)

    return parser.parse_args()


def _init_spark(task: str, execution_date: datetime.date) -> SparkSession:
    return (
        SparkSession.builder.appName(f"Web events airbyte ingestion task {task} - {execution_date.strftime('%Y%m%d')}")
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
        .enableHiveSupport()
        .getOrCreate()
    )


def main() -> None:

    args = _parse_args()
    spark = _init_spark(args.task, args.execution_date)
    config_manager = ConfigManager(args.config_file_path)

    TaskRunner(spark, config_manager, args.task, args.execution_date).run()


if __name__ == "__main__":
    main()
