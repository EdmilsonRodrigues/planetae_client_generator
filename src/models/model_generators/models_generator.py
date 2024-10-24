from src.models.model_generators.angular_model_generator import AngularModelGenerator


class ModelGenerator:
    def __new__(cls, schemas: dict[str, dict], client: str = "Angular"):
        match client:
            case "Angular":
                return AngularModelGenerator(schemas=schemas)
            case _:
                raise ValueError(f"The client for {client} is not yet implemented")
