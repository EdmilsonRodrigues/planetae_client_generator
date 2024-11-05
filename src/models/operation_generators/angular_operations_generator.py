from typing import Any
from src.models.model_generators.base_models_generator import BaseModelGenerator
from src.models.operation_generators.base_operations_generator import (
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

    schema = {
        "/api/client/contents/": {
            "get": {
                "tags": ["Contents"],
                "summary": "List Content",
                "description": "Retrieve a list of contents.\n\nParameters:\n- paginated_response (PaginatedResults): \
The paginated results.\n\nReturns:\n- PaginatedJSONResponse: The paginated results.",
                "operationId": "list_content",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
                    {
                        "name": "page",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "description": "The page number",
                            "default": 0,
                            "title": "Page",
                        },
                        "description": "The page number",
                    },
                    {
                        "name": "size",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "description": "The page size",
                            "default": 10,
                            "title": "Size",
                        },
                        "description": "The page size",
                    },
                    {
                        "name": "sort",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "description": "The sort field",
                            "default": "_id",
                            "title": "Sort",
                        },
                        "description": "The sort field",
                    },
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
                    {
                        "name": "search",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "description": "The search term",
                            "default": "",
                            "title": "Search",
                        },
                        "description": "The search term",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            },
            "post": {
                "tags": ["Contents"],
                "summary": "Create Content",
                "description": "Create new content.\n\nParameters:\n- content (Content): The content to be created. \
Do not insert the id nor _id nor owner.\n- session_and_subscription (SessionSubscription): The session and subscription\
 details.\n\nReturns:\n- ORJSONResponse: The created content.",
                "operationId": "create_content",
                "security": [{"OAuth2PasswordBearer": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ContentRequest",
                                "description": "The content to be created. Do not insert the id nor _id nor owner",
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Content"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            },
        },
        "/api/client/contents/byteam/{account_id}": {
            "get": {
                "tags": ["Contents"],
                "summary": "List Content By Accounid",
                "description": "Retrieve a list of contents by account ID.\n\nParameters:\n- paginated_response\
 (PaginatedResults): The paginated results.\n\nReturns:\n- PaginatedJSONResponse: The paginated results.",
                "operationId": "list_content_by_accounId",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
                    {
                        "name": "account_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "description": "The id of the account that owns the content",
                            "title": "Account Id",
                        },
                        "description": "The id of the account that owns the content",
                    },
                    {
                        "name": "page",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "description": "The page number",
                            "default": 0,
                            "title": "Page",
                        },
                        "description": "The page number",
                    },
                    {
                        "name": "size",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "description": "The page size",
                            "default": 10,
                            "title": "Size",
                        },
                        "description": "The page size",
                    },
                    {
                        "name": "sort",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "description": "The sort field",
                            "default": "_id",
                            "title": "Sort",
                        },
                        "description": "The sort field",
                    },
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
                    {
                        "name": "search",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "description": "The search term",
                            "default": "",
                            "title": "Search",
                        },
                        "description": "The search term",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/api/client/contents/{content_id}": {
            "get": {
                "tags": ["Contents"],
                "summary": "Read Content",
                "description": "Retrieve content by its ID.\n\nParameters:\n- content (dict): The content details from\
 the dependency.\n\nReturns:\n- ORJSONResponse: The content details.",
                "operationId": "read_content",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
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
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Content"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            },
            "put": {
                "tags": ["Contents"],
                "summary": "Update Content",
                "description": "Update content by its ID.\n\nParameters:\n- db_content (dict): The content details from\
 the dependency.\n- content (Content): The updated content. Do not insert _id nor owner.\n\nReturns:\n- ORJSONResponse:\
 The updated content.",
                "operationId": "update_content",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
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
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Content",
                                "description": "The updated content. Do not insert _id nor owner.",
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Content"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            },
            "delete": {
                "tags": ["Contents"],
                "summary": "Delete Content",
                "description": "Delete content by its ID.\n\nParameters:\n- content (dict): The content details\
 from the dependency.\n\nReturns:\n- ORJSONResponse: A response indicating the status of the deletion.",
                "operationId": "delete_content",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
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
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ActionModel"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            },
        },
        "/api/client/contents/{content_id}/detection_string": {
            "post": {
                "tags": ["Contents"],
                "summary": "Add Content Detection Strings",
                "description": "Add a detection string to content.\n\nParameters:\n- db_content (dict):\
 The content details from the dependency.\n- detectionString (str): The detection string.\n\nReturns:\n- \
ORJSONResponse: A response indicating the status of the operation.",
                "operationId": "add_content_detection_strings",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
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
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_add_content_detection_strings"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Content"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/api/client/contents/{content_id}/detection_string/{detectionString}": {
            "delete": {
                "tags": ["Contents"],
                "summary": "Delete Content Detection Strings",
                "description": "Delete a detection string from content.\n\nParameters:\n- db_content (dict): The content details from the dependency.\n- detectionString (str): The detection string.\n\nReturns:\n- ORJSONResponse: A response indicating the status of the operation.",
                "operationId": "delete_content_detection_strings",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
                    {
                        "name": "detectionString",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "description": "The detection string",
                            "title": "Detectionstring",
                        },
                        "description": "The detection string",
                    },
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
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Content"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/api/client/contents/{content_id}/allowed_domain": {
            "post": {
                "tags": ["Contents"],
                "summary": "Add Content Allowed Domains",
                "description": "Add an allowed domain to content.\n\nParameters:\n- db_content (dict): The content details from the dependency.\n- allowedDomain (str): The allowed domain.\n\nReturns:\n- ORJSONResponse: A response indicating the status of the operation.",
                "operationId": "add_content_allowed_domains",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
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
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_add_content_allowed_domains"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Content"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/api/client/contents/{content_id}/allowed_domain/{allowedDomain}": {
            "delete": {
                "tags": ["Contents"],
                "summary": "Delete Content Allowed Domains",
                "description": "Delete an allowed domain from content.\n\nParameters:\n- db_content (dict): The content details from the dependency.\n- allowedDomain (str): The allowed domain.\n\nReturns:\n- ORJSONResponse: A response indicating the status of the operation.",
                "operationId": "delete_content_allowed_domains",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
                    {
                        "name": "allowedDomain",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "description": "The allowed domain",
                            "title": "Alloweddomain",
                        },
                        "description": "The allowed domain",
                    },
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
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Content"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/api/client/contents/{content_id}/infringement-preferences": {
            "patch": {
                "tags": ["Contents"],
                "summary": "Update Infringement Preferences",
                "description": "Update the infringement preferences of content.\n\nParameters:\n- db_content (dict): The content details from the dependency.\n- infringement_preferences (dict): The infringement preferences.\n\nReturns:\n- ORJSONResponse: The updated content.",
                "operationId": "update_infringement_preferences",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
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
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/fastapi___compat__Body_update_infringement_preferences__1"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ActionModel"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/api/client/contents/{content_id}/files": {
            "post": {
                "tags": ["Contents"],
                "summary": "Upload Content Files",
                "description": "Upload files to content.\n\nParameters:\n- db_content (dict): The content details from the dependency.\n- files (list[UploadFile]): The list of files to upload.\n\nReturns:\n- ORJSONResponse: A response indicating the status of the upload.",
                "operationId": "upload_content_files",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
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
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_upload_content_files"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ActionModel"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/api/client/contents/uploads/{content_id}/{file_name}": {
            "get": {
                "tags": ["Contents"],
                "summary": "Get Content File",
                "description": "Retrieve a specific file associated with content.\n\nParameters:\n- content_id (str): The ID of the content.\n- file_name (str): The name of the file.\n\nReturns:\n- FileResponse: The requested file.",
                "operationId": "get_content_file",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
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
                    },
                    {
                        "name": "file_name",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string", "title": "File Name"},
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/api/client/contents/{content_id}/files/{file_name}": {
            "delete": {
                "tags": ["Contents"],
                "summary": "Delete File",
                "description": "Delete a file associated with content.\n\nParameters:\n- content (dict): The content details from the dependency.\n- file_name (str): The name of the file.\n\nReturns:\n- ORJSONResponse: A response indicating the status of the deletion.",
                "operationId": "delete_file",
                "security": [{"OAuth2PasswordBearer": []}],
                "parameters": [
                    {
                        "name": "file_name",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string", "title": "File Name"},
                    },
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
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ActionModel"}
                            }
                        },
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
    }

    print(angular.generate_operation(name="contents", schema=schema))
