from __future__ import annotations
from pathlib import Path
from typing import Any

from .config_legacy import Config # noqa - reexport
from .config_legacy import ServerInfo # noqa - reexport
from .config_legacy import update_config_from_ini # noqa - reexport
from .config_legacy import DEFAULT_CONFIG # noqa - reexport


def from_inifile_to_dict(path: Path) -> dict[str, Any]:
    from copy import deepcopy
    from inifile import IniFile

    values = deepcopy(DEFAULT_CONFIG)
    update_config_from_ini(values, IniFile(path))
    return values


if __name__ == "__main__":
    from json import dumps
    data = from_inifile_to_dict(Path("./tests/demo-project/Website.lektorproject"))
    print(dumps(data, indent=2))
