import json
import os
import yaml
import requests
import jsonref
from src.core.generators.open_api.generator.generator import Generator
from src.core.generators.open_api.deployer import Deployer
from src.core.generators.open_api.OOP_generator.oopgenerator import \
    OOPGenerator


class UpdateAction:
    def __init__(self):
        self.input_path = None
        self.input_spec = None
        # Dereference the spec
        self.idl = None

    def set_input_path(self, input_path):
        self.input_path = input_path

    def dereference_spec(self):
        self.idl = jsonref.JsonRef.replace_refs(self.input_spec)

    def load_idl_document(self):
        if self.input_path is None:
            raise ValueError("Invalid input path")
        if self.input_path.startswith("http"):
            self.input_spec = self.load_idl_document_from_url(self.input_path)
        else:
            self.input_spec = self.load_idl_document_from_filepath(
                self.input_path)

    def load_idl_document_from_filepath(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError("Invalid file path")

        if file_path.endswith(".yaml") or file_path.endswith(".yml"):
            return yaml.safe_load(open(file_path, 'r'))
        elif file_path.endswith(".json"):
            return json.load(open(file_path, 'r'))
        else:
            raise ValueError("Invalid file type")

    def load_idl_document_from_url(self, url):
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            raise ValueError("Invalid URL")

        content = response.content.decode("utf-8")
        if not (content.startswith("{") or content.startswith(
                "openapi") or content.startswith("asyncapi")):
            raise ValueError("Invalid IDL document")

        if url.endswith(".yaml") or url.endswith(".yml"):
            return yaml.safe_load(content)
        elif url.endswith(".json"):
            return json.loads(content)
        else:
            raise ValueError("Invalid file type")

    def update(self, generator):
        if self.idl is None:
            return

        if "openapi" in self.idl:
            if self.idl["openapi"].startswith("3.0"):
                self.handle_openapi(generator)
            else:
                print("Only OpenAPI 3.0.x is supported")
        elif "asyncapi" in self.idl:
            self.handle_asyncapi(generator)

    def handle_openapi(self, generator):
        generator.generate_client_file_obj()
        generator.generate_client_code()

        deployer = Deployer(generator)
        deployer.deploy_clients()

    def handle_asyncapi(self, generator):
        print("AsyncAPI")
        # TODO: call the asyncapi code generator

    def get_panel_classes(self):
        return self.panel_classes
