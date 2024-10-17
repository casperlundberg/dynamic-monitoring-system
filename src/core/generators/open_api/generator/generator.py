def remove_slash_from_string(string: str):
    return string.replace("/", "")


# def get_value_between_curly_brackets(string: str):
#     return string.split("{")[1].split("}")[0]

# def get_list_of_values_between_curly_brackets(string: str):
#     return [part.split("}")[0] for part in string.split("{")[1:]]

def get_dict_of_values_between_curly_brackets(string: str):
    return {part.split("}")[0]: 0 for part in string.split("{")[1:]}


def capitalize_first_letter(string: str):
    return string[0].upper() + string[1:]


class Generator:
    def __init__(self, spec: dict):
        self.spec = spec
        self.files = []

    def add_imports(self):
        paths = self.spec.get("paths")
        self.code += "import requests\n"
        self.code += f'"from src.generated_code.models.{filename} import {schema}\n"'
        self.code += "from src.core.ui import ui\n"

    def generate_server_url_variable(self, index: int):
        server_url = "server_url = " + self.spec.get("servers")[index].get(
            "url")
        return server_url

    def generate_path_url_variable(self, path: str):
        path_url = "path_url = " + f'"{path}"'
        return path_url

    def generate_parameters(self):
        params = ""
        for param in self.spec.paths.get(path).get("parameters"):
            params += f'{param.get("name")} = ' + f'"{param.get("value")}"\n'
        return params


class PathsGenerator:
    def __init__(self, paths: dict):
        self.paths = paths
        self.imports = ""
        self.url = ""
        self.parameters = {}

    def generate(self):
        for path in self.paths:

            if

            if "{" and "}" in path:
                self.parameters = get_dict_of_values_between_curly_brackets(
                    path)
            self.url = path

            filename = remove_slash_from_string(path)
            classname = capitalize_first_letter(filename)
            self.imports = self.generate_imports(filename, classname)

            self.generate_parameters(self.parameters)

    def generate_parameters(self, input_param: dict):
        for param in input_param:
            if param in self.parameters:
                self.parameters[param] = input_param.get(param)

    def generate_imports(self, filename: str, classname: str):
        code = "import requests\n"
        code += "from src.core.ui import ui\n"
        code += f'"from src.generated_code.models.{filename} import {classname}\n"'
