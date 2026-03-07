import io
from pathlib import Path
import dataclasses as dc



@dc.dataclass
class IniFile:
    filename: Path
    is_new: bool = False

    def __post_init__(self):
        from configparser import ConfigParser
        self.filename = Path(self.filename).absolute()
        self.config = ConfigParser()
        self.is_new = not bool(self.config.read(self.filename))

    def __iter__(self):
        for section in self.config.sections():
            for option in self.config.options(section):
                yield f"{section}.{option}"

    def __getitem__(self, name):
        return self.get(name)

    def get(self, name: str, default: Any = None) -> None:
        section, _, option = name.rpartition(".")
        if section not in self.config.sections():
            return default
        return self.config[section].get(option, default)

    def section_as_dict(self, name: str):
        result = {}
        for section in self.config.sections():
            if section != name:
                continue
            for option in self.config[section]:
                result[option] = self.config[section][option]
        return result

    def __setitem__(self, name, value):
        section, _, option = name.rpartition(".")
        if section not in self.config.sections():
            self.config.add_section(section)
        self.config[section][option] = value
        return value

    def save(self):
        buffer = io.StringIO()
        self.config.write(buffer)
        self.filename.write_text(buffer.getvalue())
