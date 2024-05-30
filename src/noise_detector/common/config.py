from dataclasses import dataclass
from typing import Any, Self

import yaml

DEFAULT_CONFIG_PATH = "./config/config.yaml"


@dataclass
class Config:
    """Sample config load implementation."""
    rate: int
    chunk: int
    channels: int
    rms_detection_value: int

    @classmethod
    def load_config(cls) -> Self:
        return cls(**_read_yaml(DEFAULT_CONFIG_PATH))


def _read_yaml(path: str) -> Any:
    with open(path, "rb") as file:
        return yaml.safe_load(file)