from abc import ABC, abstractmethod
from typing import Any


class BaseOperationGenerator(ABC):
    paths: dict[str, dict]

    def __init__(self, paths: dict[str, dict]) -> None:
        self.paths = paths

    @classmethod
    @abstractmethod
    def generate_operation(cls, name: str, schema: dict[str, Any]) -> str:
        pass

    def get_common_parts(self) -> list[str]:
        paths = self.paths.keys()
        first_path = list(paths)[0]
        splitted_path = first_path.split("/")
        common_parts = []
        for part in splitted_path:
            if all(part in path for path in paths):
                common_parts.append(part)
            else:
                break
        return common_parts

    def group_operations(self) -> dict[str, dict[str, dict]]:
        common_parts = self.get_common_parts()
        groups: dict[str, dict[str, dict]] = {}
        for path in self.paths:
            for part in path.split("/"):
                if part not in common_parts:
                    if part in groups:
                        groups[part].update({path: self.paths[path]})
                    else:
                        groups[part] = {path: self.paths[path]}
        return groups

    def generate_operations(self) -> str:
        models = ""
        for name, schema in self.schemas.items():
            models += f"{self.generate_model(self.format_name(name), schema)}\n\n"
        return models
