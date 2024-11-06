import multiprocessing
import os
import orjson
from models.model_generators.base_models_generator import BaseModelGenerator
from models.model_generators.models_generator import ModelGenerator
from models.operation_generators.base_operations_generator import (
    BaseOperationGenerator,
)
from models.operation_generators.operations_generator import OperationGenerator


class ClientGenerator:
    models_generator: BaseModelGenerator
    operations_generator: BaseOperationGenerator
    openapi: dict

    def __init__(
        self, src_path: str, output_path: str, client: str = "angular"
    ) -> None:
        with open(src_path, "r") as f:
            self.openapi = orjson.loads(f.read())
        self.models_generator = ModelGenerator(
            schemas=self.openapi["components"]["schemas"], client=client
        )
        self.operations_generator = OperationGenerator(
            self.openapi["paths"], client=client
        )
        self.output_path = output_path

    def generate_client(self):
        api_folder = os.path.join(self.output_path, "api")
        os.makedirs(api_folder, exist_ok=True)
        models_path = os.path.join(api_folder, "models.ts")
        services_folder = os.path.join(api_folder, "services")
        os.makedirs(services_folder, exist_ok=True)
        models_subprocess = multiprocessing.Process(
            target=self.generate_models, args=(models_path,)
        )
        services_multiprocess = multiprocessing.Process(
            target=self.generate_services, args=(services_folder,)
        )
        models_subprocess.start()
        services_multiprocess.start()

    def generate_models(self, models_path: str):
        with open(models_path, "w") as f:
            for model in self.models_generator.generate_models():
                f.write(model)

    def generate_services(self, services_folder: str):
        for operation, content in self.operations_generator.generate_operations():
            with open(os.path.join(services_folder, f"{operation}.ts"), "w") as f:
                f.write(content)
