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

    def get(self, name, default: Any = None) -> None:
        section, _, option = name.rpartition(".")
        if section not in self.config.sections():
            return fallback
        return self.config[section].get(option)
