# python -m lektor.environment.config_new
from __future__ import annotations

from pathlib import Path
import json

import pydantic
from .types import ListOfStringsType


DEFAULTS = json.loads((Path(__file__).parent / "config.json").read_text())


class Config(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")
    
    ephemeral_record_cache_size: int = pydantic.Field(ge=0, alias="EPHEMERAL_RECORD_CACHE_SIZE")
    attachment_types: dict[str, str] = pydantic.Field(default=DEFAULTS["attachment_types"], alias="ATTACHMENT_TYPES")
    themes: ListOfStringsType = pydantic.Field(default_factory=list)
    pass


if __name__ == "__main__":
    from pathlib import Path
    from sys import argv
    from json import loads

    data = loads(Path("tests/demo-project/Website.lektorproject.json" if len(argv) == 1 else argv[1]).read_text()) 
    cfg = Config(**data)   
