from typing import Any
from src.models.operation_generators.base_operations_generator import (
    BaseOperationGenerator,
)


class AngularOperationGenerator(BaseOperationGenerator):
    @classmethod
    def generate_operation(cls, name: str, schema: dict[str, Any]) -> str:
        return super().generate_operation(name, schema)
