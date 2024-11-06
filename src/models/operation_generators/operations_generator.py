from models.operation_generators.angular_operations_generator import (
    AngularOperationGenerator,
)


class OperationGenerator:
    def __new__(cls, paths: dict[str, dict], client: str = "Angular"):
        match client:
            case "Angular":
                return AngularOperationGenerator(paths)
            case _:
                raise ValueError(f"The client for {client} is not yet implemented")
