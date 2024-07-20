"""Test for the FHIR API functions."""

from pathlib import Path

import yaml

from utils.fhir_api import build_url, load_config


def test_load_config(tmp_path) -> None:
    """Test for the load_config function."""
    config_data = {
        "fhir_api_base": "https://github.com/",
        "endpoints": {"search": "octocat?tab=following"},
    }
    config_file = Path(tmp_path / "settings.yml")

    with Path(config_file).open("w", encoding="utf-8") as file_:
        yaml.dump(config_data, file_)

    loaded_config = load_config(config_file_path=config_file)

    assert loaded_config == config_data


def test_build_url() -> None:
    """Test for the build_url function."""
    config_data = {
        "fhir_api_base": "https://github.com/",
        "endpoints": {"search": "octocat?tab=following"},
    }

    expected_url = "https://github.com/octocat?tab=following"

    assert build_url(config_data, "search") == expected_url
