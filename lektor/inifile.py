from configparser import ConfigParser, MissingSectionHeaderError
import dataclasses as dc
import io
from pathlib import Path
from typing import Any, Iterator
import pickle
import os


def config_parser_load(filename: str | Path) -> tuple[ConfigParser, bool]:
    path = Path(filename)
    config = ConfigParser()
    try:
        return config, not bool(config.read(path))
    except MissingSectionHeaderError:
        text = path.read_text()
        config.read_string(f"[DEFAULT]\n{text}")
        return config, False



@dc.dataclass
class IniFileNew:
    filename: str
    is_new: bool = False

    def __post_init__(self) -> None:

        #self.filename = Path(self.filename).absolute()
        self.filename = os.path.abspath(self.filename)

        self.config, self.is_new = config_parser_load(self.filename)

    def __iter__(self) -> Iterator[str]:
        for section in self.config.sections():
            for option in self.config.options(section):
                yield f"{section}.{option}"

    def __getitem__(self, name: str) -> Any:
        return self.get(name)

    def items(self):
        if not self.config.sections():
            return self.config.defaults().items()
        raise RntimeError("cannot call .items")

    def sections(self) -> list[str]:
        return self.config.sections()

    def get(self, name: str, default: Any = None) -> Any:
        section, _, option = name.rpartition(".")
        if section not in self.sections():
            return default
        return self.config[section].get(option, default)

    def section_as_dict(self, name: str) -> dict[str, Any]:
        result = {}
        for section in self.sections():
            if section != name:
                continue
            for option in self.config[section]:
                result[option] = self.config[section][option]
        return result

    def __setitem__(self, name: str, value: Any) -> None:
        section, _, option = name.rpartition(".")
        if section not in self.sections():
            self.config.add_section(section)
        self.config[section][option] = value

    def get_int(self, name: str, default: Any = None) -> bool | None:
        value = self.get(name, default)
        if value is None:
            return None
        return int(value)

    def get_bool(self, name: str, default: Any = False) -> bool | None:
        value = self.get(name)
        if value is None:
            return None
            breakpoint()
            raise KeyError(f"cannot find boolean in {name}")
        return bool({
            "0": False,
            "no": False,
            "false": False,
            "1": True,
            "yes": True,
            "true": True,
        }.get(value, default))


    def save(self) -> None:
        buffer = io.StringIO()
        self.config.write(buffer)
        self.filename.write_text(buffer.getvalue())

"""
{
  "__getattr__": [
    "items",
    "get",
    "get_bool",
    "get_int",
    "is_new",
    "sections",
    "section_as_dict",
    "save",
    "filename"
  ],
  "__getitem__": [
    "theme.name",
    "alternatives.de.name[de]",
    "alternatives.en.name[de]",
    "test_setting",
    "author.name",
    "model.name",
    "author.email",
    "model.label",
    "alternatives.en.name",
    "alternatives.de.name",
    "block.name"
  ],
  "__setitem__": [
    "packages.lektor-webpack-support",
    "is_cached"
  ]
}
"""


class IniFileRecord:
    def __init__(self, *args, **kwargs):
        from inifile import IniFile as IF
        from pathlib import Path
        self._class = IF(*args, **kwargs)
        self._fp = Path("/Users/antonio/Projects/contabo/website/dev/lektor/out.txt")

    def _xread(self):
        data = {
            "__getattr__": set(),
            "__getitem__": set(),
            "__setitem__": set(),
        }
        if self._fp.exists():
            data = pickle.loads(self._fp.read_bytes())
        return data

    def _xwrite(self, data):
        self._fp.write_bytes(pickle.dumps(data))


    def __getattr__(self, name):
        data = self._xread()
        data["__getattr__"].add(name)
        self._xwrite(data)
        return getattr(self._class, name)

    def __iter__(self):
        return getattr(self._class, "__iter__")()

    def __getitem__(self, name):
        data = self._xread()
        data["__getitem__"].add(name)
        self._xwrite(data)
        return self._class[name]

    def __setitem__(self, name, value):
        data = self._xread()
        data["__setitem__"].add(name)
        self._xwrite(data)
        self._class[name] = value



IniFile = IniFileNew
