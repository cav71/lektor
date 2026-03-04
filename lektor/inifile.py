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

    def get(self, key, fallback: Any = None):
        section, _, option = key.partition(".")
        if key == "project.path":
            return self.filename

        if section not in self.config.sections():
            return fallback
        return self.config[section].get(option)
