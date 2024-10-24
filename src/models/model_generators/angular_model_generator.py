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
    content_dict = {
        "properties": {
            "updatedAt": {
                "type": "string",
                "format": "date-time",
                "title": "Updatedat",
                "default": "2024-10-23T20:01:54.541556Z",
            },
            "_id": {
                "type": "string",
                "title": " Id",
                "default": "67194822bc05a0a474c246be",
            },
            "title": {"type": "string", "title": "Title", "default": ""},
            "type": {"type": "string", "title": "Type", "default": ""},
            "modelName": {"type": "string", "title": "Modelname", "default": ""},
            "description": {
                "type": "string",
                "title": "Description",
                "default": "",
            },
            "metadata": {"type": "object", "title": "Metadata", "default": {}},
            "owner": {"type": "string", "title": "Owner", "default": ""},
            "owner_email": {
                "type": "string",
                "title": "Owner Email",
                "default": "",
            },
            "owner_name": {"type": "string", "title": "Owner Name", "default": ""},
            "accountId": {"type": "string", "title": "Accountid", "default": ""},
            "imagePreview": {
                "type": "string",
                "title": "Imagepreview",
                "default": "",
            },
            "urls": {
                "items": {"type": "string"},
                "type": "array",
                "title": "Urls",
                "default": [],
            },
            "tags": {
                "items": {"type": "string"},
                "type": "array",
                "title": "Tags",
                "default": [],
            },
            "infringementPreferences": {
                "$ref": "#/components/schemas/InfringementPreferences",
                "default": {
                    "updatedAt": "2024-10-23T20:01:54.541556Z",
                    "receiveEmailOnDetection": False,
                    "automaticApproveInfringements": False,
                    "receiveEmailOnTakedown": False,
                    "sendTakedownRequests": False,
                },
            },
            "detectionStrings": {
                "items": {"type": "string"},
                "type": "array",
                "title": "Detectionstrings",
                "default": [],
            },
            "allowedDomains": {
                "items": {"type": "string"},
                "type": "array",
                "title": "Alloweddomains",
                "default": [],
            },
            "files": {
                "items": {"type": "string"},
                "type": "array",
                "title": "Files",
                "default": [],
            },
            "is_verified": {
                "type": "boolean",
                "title": "Is Verified",
                "default": False,
            },
            "createdAt": {
                "type": "string",
                "format": "date-time",
                "title": "Createdat",
                "default": "2024-10-23T20:01:54.541556Z",
            },
            "country": {"type": "string", "title": "Country", "default": ""},
            "company": {"type": "string", "title": "Company", "default": ""},
            "signature": {"type": "string", "title": "Signature", "default": ""},
        },
        "type": "object",
        "title": "Content",
        "description": "Represents a piece of content.\n\nAttributes:\n    id (PyObjectId): The unique identifier for the content.\n    title (str): The title of the content.\n    type (str): The type of the content.\n    description (str): The description of the content.\n    metadata (Dict[str, Any]): Additional metadata associated with the content.\n    owner (str): The owner of the content.\n    imagePreview (Optional[str]): The URL of the image preview for the content.\n    url (Optional[str]): The URL of the content.\n    tags (List[str]): The tags associated with the content.\n    infringementPreferences (InfringementPreferences): The infringement preferences for the content.\n    detectionStrings (List[str]): The detection strings for the content.\n    allowedDomains (List[str]): The allowed domains for the content.\n    files (List[str]): The files associated with the content.\n    is_verified (bool): Indicates whether the content is verified.\n    updatedAt (datetime): The date and time when the content was last updated.\n    createdAt (datetime): The date and time when the content was created.",
    }

    print(AngularModelGenerator({}).generate_model("Content", content_dict))
