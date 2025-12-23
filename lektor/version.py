from pathlib import Path
from importlib import metadata


def get_version() -> str:
    try:
        return metadata.version("Lektor")
    except metadata.PackageNotFoundError:
        return "unknown"
