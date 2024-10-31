from abc import abstractmethod, ABC
from typing import Any, Generator


class BaseModelGenerator(ABC):
    schemas: dict[str, dict]

    def __init__(self, schemas: dict[str, dict]) -> None:
        self.schemas = schemas

    @classmethod
    @abstractmethod
    def generate_model(cls, name: str, schema: dict[str, Any]) -> str:
        pass

    @staticmethod
    def capitalize(string: str) -> str:
        if string:
            return string[0].upper() + string[1:]
        return ""

    @classmethod
    def format_name(cls, name: str) -> str:
        name = name.replace("_", " ").replace("-", " ")
        return "".join(cls.capitalize(part) for part in name.split(" "))

    def generate_models(self) -> Generator[str, None, None]:
        for name, schema in self.schemas.items():
            yield f"{self.generate_model(self.format_name(name), schema)}\n\n"
