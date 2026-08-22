from pathlib import Path

import yaml


CONFIG_DIR = Path(__file__).parent.parent / "config"


def load_yaml(filename: str) -> dict:
    """Load a YAML configuration file."""

    path = CONFIG_DIR / filename

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_sources() -> dict:
    """Load sources.yaml"""
    return load_yaml("sources.yaml")


def load_search() -> dict:
    """Load search.yaml"""
    return load_yaml("search.yaml")