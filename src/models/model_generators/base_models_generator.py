from abc import abstractmethod, ABC
from typing import Any


class BaseModelGenerator(ABC):
    def __init__(self, schemas: dict[str, dict]) -> None:
        self.schemas = schemas

    @classmethod
    @abstractmethod
    def generate_model(cls, name: str, schema: dict[str, Any]) -> str:
        pass

    @staticmethod
    def format_name(name: str) -> str:
        return name.replace("_", " ").replace("-", " ").title().replace(" ", "")

    def generate_models(self) -> str:
        models = ""
        for name, schema in self.schemas.items():
            models += f"{self.generate_model(self.format_name(name), schema)}\n\n"
        return models
