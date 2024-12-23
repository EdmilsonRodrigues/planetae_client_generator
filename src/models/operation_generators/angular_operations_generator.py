import re
from typing import Any
from models.operation_generators.base_operations_generator import (
    BaseOperationGenerator,
)
from models.parameters import Parameters
from models.model_generators.base_models_generator import BaseModelGenerator


class AngularOperationGenerator(BaseOperationGenerator):
    tab: str = "  "

    @classmethod
    def get_parameters(
        cls, parameters: list[dict], request_body: dict, responses: dict
    ) -> Parameters:
        param = Parameters(
            parameters=parameters, request_body=request_body, responses=responses
        )
        return param

    @classmethod
    def generate_function(
        cls, path: str, method: str, name: str, schema: dict[str, Any]
    ) -> str:
        parameters = cls.get_parameters(
            schema.get("parameters", []),
            schema.get("requestBody", {}),
            schema.get("responses", {}),
        )
        responses = parameters.get_responses()
        func = (
            f"""
{cls.tab}{name} ({parameters}): Observable<{responses}>"""
            + " {\n"
        )

        func += f"{cls.tab}{cls.tab}const params = new HttpParams()\n"
        for query, variable, question_mark in parameters.get_queries():
            if question_mark:
                func += f"{cls.tab}{cls.tab}if ({variable} !== null) " + "{\n" + cls.tab
            func += f"{cls.tab}{cls.tab}params.set('{query}', {variable}.toString())\n"
            if question_mark:
                func += cls.tab + cls.tab + "}\n"

        func += "\n"

        func += f"{cls.tab}{cls.tab}return this.http.{method}<{responses}>\
(`${{this.apiUrl}}{cls.format_path(path=path)}`, {{ params }})"
        if "request: " in str(parameters):
            func = func[:-13] + ", " + "request" + func[-13:]
        func += "\n" + cls.tab + "}\n"
        return func

    @classmethod
    def format_path(cls, path: str) -> str:
        parameters_re = r"{\w+}"
        matches = re.findall(parameters_re, path)
        for match in matches:
            parameter = BaseModelGenerator.format_name(match)
            parameter = parameter[0].lower() + parameter[1:]
            path = path.replace(match, f"${parameter}")
        return path

    @classmethod
    def generate_functions(cls, schema: dict[str, Any]) -> str:
        content = ""
        for path, methods in schema.items():
            for method, details in methods.items():
                operation_id = details["operationId"]
                content += cls.generate_function(
                    path=path,
                    method=method,
                    name=cls.get_function_name(operation_id),
                    schema=details,
                )
        return content

    @classmethod
    def generate_operation(cls, name: str, schema: dict[str, Any]) -> str:
        content = """\
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import * as models from '../models'

@Injectable({
  providedIn: 'root'
})
"""
        content += f"export class {name.replace("-", " ").replace("_", " ").title().replace(" ", "")}Service" + " {\n"
        content += "  private apiUrl = `${environment.APIHost}`\n\n"
        content += "  constructor (private http: HttpClient) { }\n"
        content += cls.generate_functions(schema=schema)
        content += "}\n"
        return content


if __name__ == "__main__":
    import orjson

    with open("example.json", "r") as f:
        schema = orjson.loads(f.read())

    paths = schema["paths"]

    angular = AngularOperationGenerator(paths=paths)

    print(angular.generate_operation(name="contents", schema=schema))
