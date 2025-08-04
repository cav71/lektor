from typing import Annotated, Any, Callable
import pydantic


def ensure_list(sep: str = ",") -> Callable[[Any], Any]:
    def _ensure_list(value: Any) -> Any:  
        return [x.strip() for x in value.replace("\n", sep).split(sep) if x.strip()]
    return _ensure_list


ListOfStringsType = Annotated[list[str], pydantic.BeforeValidator(ensure_list())]

