import dataclasses as dc
import io
from pathlib import Path
from typing import Any, Iterator


@dc.dataclass
class IniFile:
    filename: Path
    is_new: bool = False

    def __post_init__(self) -> None:
        from configparser import ConfigParser

        self.filename = Path(self.filename).absolute()
        self.config = ConfigParser()
        self.is_new = not bool(self.config.read(self.filename))

    def __iter__(self) -> Iterator[str]:
        for section in self.config.sections():
            for option in self.config.options(section):
                yield f"{section}.{option}"

    def __getitem__(self, name: str) -> Any:
        return self.get(name)

    def get(self, name: str, default: Any = None) -> Any:
        section, _, option = name.rpartition(".")
        if section not in self.config.sections():
            return default
        return self.config[section].get(option, default)

    def section_as_dict(self, name: str) -> dict[str, Any]:
        result = {}
        for section in self.config.sections():
            if section != name:
                continue
            for option in self.config[section]:
                result[option] = self.config[section][option]
        return result

    def __setitem__(self, name: str, value: Any) -> None:
        section, _, option = name.rpartition(".")
        if section not in self.config.sections():
            self.config.add_section(section)
        self.config[section][option] = value

    def save(self) -> None:
        buffer = io.StringIO()
        self.config.write(buffer)
        self.filename.write_text(buffer.getvalue())
