from typing import Generator
from models.model_generators.base_models_generator import BaseModelGenerator


class Parameters:
    query_parameters: list = []
    path_parameters: list = []
    request_body: dict
    responses: dict

    def __init__(self, parameters: list, request_body: dict, responses: dict) -> None:
        self.query_parameters = []
        self.path_parameters = []
        for parameter in parameters:
            match parameter["in"]:
                case "query":
                    self.query_parameters.append(parameter)
                case "path":
                    self.path_parameters.append(parameter)
        self.request_body = request_body
        self.responses = responses

    def get_queries(self) -> Generator[tuple[str, str, bool], None, None]:
        for query in self.query_parameters:
            var = self.get_parameter_string(query, no_default=True)
            question_mark = False
            if "null" in var.split(':')[1]:
                question_mark = True
            var = self.get_parameter_string(query, no_default=True, only_name=True)
            yield (var, var, question_mark)

    def get_parameters_str(self):
        string = ""
        for query in self.query_parameters:
            string += self.get_parameter_string(query) + ", "
        for path in self.path_parameters:
            string += self.get_parameter_string(path) + ", "
        return string[:-2]

    def get_request_body_str(self):
        string = ""
        body_item = self.request_body.get("content", None)
        required = self.request_body.get("required", False)
        if body_item is None:
            return None
        string += self.get_body_item_string(body_item)
        if not required:
            string += " | null = null"
        return string

    def get_responses(self) -> str:
        positive_responses = [
            self.responses[response]
            for response in self.responses
            if int(response) // 100 == 2
        ]
        responses_str = " | ".join(
            self.get_response(response) for response in positive_responses
        )
        return responses_str

    def get_response(self, response: dict) -> str:
        try:
            schema = response["content"]["application/json"]["schema"]
        except KeyError:
            return "null"
        try:
            return "models." + BaseModelGenerator.format_name(
                schema["$ref"].split("/")[-1]
            )
        except KeyError:
            return self.get_parameter_type(schema)

    @classmethod
    def get_body_item_string(cls, schema: dict) -> str:
        try:
            multipart = schema.get("multipart/form-data", None)
            if multipart is not None:
                return (
                    "request: "
                    + "models."
                    + BaseModelGenerator.format_name(
                        multipart["schema"]["$ref"].split("/")[-1]
                    )
                )
            type = cls.get_request_body_type(schema["application/json"]["schema"])
            name = "request"
            string = f"{name}: {type}"
        except KeyError:
            form = schema.get("application/x-www-form-urlencoded", None)
            if form is not None:
                string = (
                    "request: "
                    + "models."
                    + BaseModelGenerator.format_name(
                        form["schema"]["$ref"].split("/")[-1]
                    )
                )
            else:
                print(schema)
                raise
        return string

    @classmethod
    def get_parameter_type(cls, schema: dict, array: bool = False) -> str:
        type = schema.get("type", None)
        match type:
            case None:
                anyof = schema.get("anyOf", None)
                ref = schema.get("$ref", None)
                if anyof is not None:
                    type = " | ".join(
                        cls.get_parameter_type(option) for option in schema["anyOf"]
                    )
                elif schema == {}:
                    type = "any"
                elif ref is not None:
                    type = "models." + BaseModelGenerator.format_name(
                        ref.split("/")[-1]
                    )
                else:
                    raise NotImplementedError(schema)
            case "integer" | "number":
                type = "number"
            case "string":
                type = "string"
            case "boolean":
                type = "boolean"
            case "null":
                type = "null"
            case "array":
                items = schema["items"]
                type = cls.get_parameter_type(items, array=True)
            case _:
                raise NotImplementedError(schema)
        if array:
            type = " | ".join(f"{part}[]" for part in type.split(" | "))
        return type

    @classmethod
    def get_request_body_type(cls, schema: dict) -> str:
        type = schema.get("type", None)
        try:
            type = cls.get_parameter_type(schema)
        except NotImplementedError:
            ref = schema.get("$ref", None)
            if ref is not None:
                type = ref.split("/")[-1]
                type = "models." + BaseModelGenerator.format_name(type)
            else:
                raise NotImplementedError(schema)
        return type

    @classmethod
    def get_parameter_string(
        cls, parameter: dict, no_default: bool = False, only_name: bool = False
    ) -> str:
        if no_default:
            default = None
        else:
            default = parameter["schema"].get("default", None)
        try:
            type = cls.get_parameter_type(parameter["schema"])
            name = BaseModelGenerator.format_name(parameter["name"])
            name = name[0].lower() + name[1:]
            if only_name:
                return name
            string = f"{name}: {type}"
        except KeyError:
            print(parameter)
            raise
        if default is not None:
            if type == "string" or ("string" in type and default != "null"):
                string += f" = '{default}'"
            else:
                string += f" = {default}"
        return string

    def __str__(self) -> str:
        parameters = self.get_parameters_str()
        request_body = self.get_request_body_str()
        if parameters and request_body:
            string = f"{parameters}, {request_body}"
        elif parameters:
            string = parameters
        elif request_body:
            string = request_body
        else:
            string = ""
        return string
