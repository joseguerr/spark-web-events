import os

import pytest

from spark_web_events_etl.config_manager import ConfigException, ConfigManager


def test_read_existent_key() -> None:
    # GIVEN
    config_manager = ConfigManager(
        config_file=f"{os.path.dirname(os.path.realpath(__file__))}/fixtures/test_app_config.yaml"
    )
    value_expected = "v1"

    # WHEN
    value_output = config_manager.get("k1")

    # THEN
    assert value_output == value_expected


def test_read_inexistent_key() -> None:
    # GIVEN
    config_manager = ConfigManager(
        config_file=f"{os.path.dirname(os.path.realpath(__file__))}/fixtures/test_app_config.yaml"
    )

    # THEN
    with pytest.raises(ConfigException):
        config_manager.get("inexistent_key")


def test_inexistent_config_file() -> None:
    # GIVEN
    inexistent_config_file = "inexistent_config_file.yaml"

    # THEN
    with pytest.raises(FileNotFoundError):
        ConfigManager(config_file=inexistent_config_file)
