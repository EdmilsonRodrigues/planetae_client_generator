from typing import Any
from src.models.model_generators.base_models_generator import BaseModelGenerator


class AngularModelGenerator(BaseModelGenerator):
    @classmethod
    def get_property_type(cls, type: str | None, data: dict[str, Any]) -> str:
        match type:
            case "string":
                if data.get("format") == "date-time":
                    return "Date"
                else:
                    return "string"
            case "object":
                return "any"
            case "array":
                result = cls.get_property_type(data["items"].get("type"), data["items"])
                return " | ".join(f"{item}[]" for item in result.split(" | "))
            case "boolean":
                return "boolean"
            case "null":
                return "null"
            case "integer" | "number":
                return "number"
            case None:
                anyOf = data.get("anyOf", [])
                if anyOf:
                    return " | ".join((cls.get_property_type(option.get("type"), option) for option in anyOf))
                ref = data.get("$ref")
                if ref:
                    return ref.split("/")[-1]
                else:
                    raise ValueError(f"Not implemented way of handling data: {data}")
            case _:
                raise ValueError(f"Type {data.get("type")} not yet implemented")

    @classmethod
    def get_property_line(cls, property: str, data: dict[str, Any]) -> str:
        default = "?:" if data.get("default", None) is not None else ":"
        line = f"\t{property}{default} "
        return line + cls.get_property_type(data.get("type"), data)

    @classmethod
    def generate_model(cls, name: str, schema: dict[str, Any]) -> str:
        interface = "export interface {name} {{\n".format(name=name)
        properties: dict[str, dict] = schema.get("properties", {})
        for property, data in properties.items():
            interface += cls.get_property_line(property=property, data=data) + "\n"
        interface += "}"
        return interface


if __name__ == "__main__":
    import json

    with open("example.json") as f:
        example = json.load(f)
    
    schema = example["components"]["schemas"]

    print(AngularModelGenerator(schema).generate_models())
