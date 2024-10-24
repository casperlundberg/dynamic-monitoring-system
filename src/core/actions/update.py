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
        spec = self.load_idl_document()

        # Dereference the spec
        self.idl = jsonref.JsonRef.replace_refs(spec)
        self.ui_classnames = []

    def set_input_path(self, input_path):
        self.input_path = input_path

    def load_idl_document(self):
        if self.input_path is None:
            raise ValueError("Invalid input path")
        if self.input_path.startswith("http"):
            return self.load_idl_document_from_url(self.input_path)
        else:
            return self.load_idl_document_from_filepath(self.input_path)

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

    def update(self):
        if self.idl is None:
            return

        if "openapi" in self.idl:
            self.handle_openapi()
        elif "asyncapi" in self.idl:
            self.handle_asyncapi()

    def handle_openapi(self):
        oop_generator = OOPGenerator(self.idl)
        oop_generator.generate_client_file_obj()
        oop_generator.generate_client_code()

        oop_generator.generate_ui_file_obj()
        oop_generator.generate_ui_code()

        for ui_file in oop_generator.ui_files:
            self.ui_classnames.append(ui_file.classname)

        deployer = Deployer(oop_generator)
        deployer.deploy_clients()
        deployer.deploy_uis()

    def handle_asyncapi(self):
        print("AsyncAPI")
        # TODO: call the asyncapi code generator

    def get_panel_classes(self):
        return self.panel_classes

# Example usage
# if __name__ == "__main__":
#     action = UpdateAction("C:/Users/Desktop-Lumpa/Downloads/openapi.json")
#     action.update()
