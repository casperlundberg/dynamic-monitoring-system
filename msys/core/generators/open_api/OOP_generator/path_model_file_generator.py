from typing import Dict, Any
from msys.core.generators.open_api.OOP_generator.parameter_model_file_generator import \
    ParameterModelFileGenerator


class PathModelFileGenerator:
    def __init__(self, path_obj: Dict[str, Any]):
        self.imports = None
        self.path_obj = path_obj
        self.parameters = self.path_obj.get("parameters", [])
        self.classname = self.path_obj.get("operationId", "Path").capitalize()
        self.code_string = ""

    def generate_imports(self):
        self.imports = "from typing import List\n"

    def generate_parameter_classes(self):
        parameter_classes = []
        for param in self.parameters:
            param_gen = ParameterModelFileGenerator(param)
            param_gen.generate_imports()
            param_gen.parse_parameter()
            param_gen.parse_schema()
            param_gen.generate_schema_class()
            parameter_classes.append(param_gen.code_string)
        return "\n".join(parameter_classes)

    def generate_path_class(self):
        parameter_classes_code = self.generate_parameter_classes()
        self.code_string = f"""{self.imports}
{parameter_classes_code}

@dataclass
class {self.classname}:
    parameters: List
        """
