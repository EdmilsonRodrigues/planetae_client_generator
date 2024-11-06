from typing import Any
from models.model_generators.base_models_generator import BaseModelGenerator
from models.operation_generators.base_operations_generator import (
    BaseOperationGenerator,
)

"""
  getContents (skip: number = 0, pageSize: number = 10): Observable<PaginatedResponse<Content>> {
    const currentPage = skip // Current page number

    const getContents = (pageSize: number, currentPage: number): Observable<PaginatedResponse<Content>> => {
      const params = new HttpParams()
        .set('page', currentPage.toString())
        .set('size', pageSize.toString())

      return this.http.get<PaginatedResponse<Content>>(`${this.apiUrl}`, { params })
    }

    return getContents(pageSize, currentPage)
  }

  getOneContent (id: string): Observable<Content> {
    return this.http.get<any>(`${this.apiUrl}/${id}`)
  }

  createContent (data: any): Observable<Content> {
    return this.http.post<any>(this.apiUrl, data)
  }

  deleteFile (id: string, file: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}/files/${file}`)
  }

  getFile (id: string, file: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/uploads/${id}/${file}`, { responseType: 'blob' })
  }

  updateInfringementPreferences (contentId: string, preferences: InfringementPreferences): Observable<Content> {
    return this.http.patch<Content>(`${this.apiUrl}/${contentId}/infringement-preferences`, { preferences })
  }
"""

"""
{
    "name": "content_id",
    "in": "path",
    "required": True,
    "schema": {
        "type": "string",
        "minLength": 24,
        "maxLength": 24,
        "description": "The id of the content",
        "title": "Content Id",
    },
    "description": "The id of the content",
}
{
    "name": "order",
    "in": "query",
    "required": False,
    "schema": {
        "type": "string",
        "description": "The sort order",
        "default": "asc",
        "title": "Order",
    },
    "description": "The sort order",
},
"""


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

    def get_queries(self) -> str:
        queries = [
            f"{self.get_parameter_string(query, no_default=True, only_name=True)}=${{{self.get_parameter_string(query, no_default=True, only_name=True)}}}"
            for query in self.query_parameters
        ]
        return "&".join(queries)

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
        schema = response["content"]["application/json"]["schema"]
        try:
            return BaseModelGenerator.format_name(schema["$ref"].split("/")[-1])
        except KeyError:
            return self.get_parameter_type(schema)

    @classmethod
    def get_body_item_string(cls, schema: dict) -> str:
        try:
            multipart = schema.get("multipart/form-data", None)
            if multipart is not None:
                return "request: " + BaseModelGenerator.format_name(
                    multipart["schema"]["$ref"].split("/")[-1]
                )
            type = cls.get_request_body_type(schema["application/json"]["schema"])
            name = "request"
            string = f"{name}: {type}"
        except KeyError:
            print(schema)
            raise
        return string

    @classmethod
    def get_parameter_type(cls, schema: dict) -> str:
        type = schema.get("type", None)
        match type:
            case None:
                anyof = schema.get("anyOf", None)
                if anyof is not None:
                    type = " | ".join(
                        cls.get_parameter_type(option) for option in schema["anyOf"]
                    )
                elif schema == {}:
                    type = "any"
                else:
                    raise NotImplementedError(schema)
            case "integer":
                type = "number"
            case "string":
                type = "string"
            case "boolean":
                type = "boolean"
            case "null":
                type = "null"
            case _:
                raise NotImplementedError(schema)
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
                type = BaseModelGenerator.format_name(type)
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
            if only_name:
                return parameter["name"]
            string = f"{parameter['name']}: {type}"
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
{cls.tab}{name}({parameters}): Observable<{parameters}>"""
            + " {\n"
        )
        func += f"{cls.tab}{cls.tab}return this.http.{method}<{responses}>(`${{this.apiUrl}}{path.replace("{", "${")}?{parameters.get_queries()}`)"
        if func[-3] == "?":
            func = func[:-3] + "`)"
        func += "\n" + cls.tab + "}\n"
        return func

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
        content = """
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from '@env/environment'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'

@Injectable({
  providedIn: 'root'
})
"""
        content += f"export class {name.title()}Service" + " {\n"
        content += "  private apiUrl = `${environment.APIHost}/api/client/contents`\n\n"
        content += "  constructor (private http: HttpClient) { }\n"
        content += cls.generate_functions(schema=schema)
        content += "}"
        return content


if __name__ == "__main__":
    import orjson

    with open("example.json", "r") as f:
        schema = orjson.loads(f.read())

    paths = schema["paths"]

    angular = AngularOperationGenerator(paths=paths)

    print(angular.generate_operation(name="contents", schema=schema))
