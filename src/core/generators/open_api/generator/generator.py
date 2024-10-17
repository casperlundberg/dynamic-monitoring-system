def replace_slash(string: str):
    return string.replace("/", "_")


def remove_brackets(string: str):
    return string.replace("{", "").replace("}", "")


def get_dict_of_path_params(string: str):
    return {part.split("}")[0]: 0 for part in string.split("{")[1:]}


def get_dict_of_query_params(string: str):
    query_string = string.split("?")[1] if "?" in string else ""
    return {param.split("=")[0]: None for param in query_string.split("&") if
            "=" in param}


def capitalize_first_letter(string: str):
    return string[0].upper() + string[1:]


class Generator:
    def __init__(self, spec: dict):
        self.spec = spec
        self.files = []

    def generate(self):
        paths = self.spec.get("paths")
        for path in paths:
            path_str = str(path)
            path_obj = paths[path]
            server_url = self.spec.get("servers")[0].get("url")
            file_gen = CodeFileGenerator(path_obj, path_str, server_url)

            code_string = file_gen.generate_code()

            if code_string is None:
                continue
            print("====================================")
            print("Code generated for path:", path_str)
            print("Will be saved in file:",
                  file_gen.filename + ".py with a dataclass named ",
                  file_gen.classname)
            print("http method:", file_gen.http_method)
            print()
            print(code_string)
            print()
            print()
            print()


class CodeFileGenerator:
    def __init__(self, path: dict, path_str, server_url: str):
        self.path = path
        self.path_str = path_str
        self.server_url = server_url
        self.imports = None
        self.url = server_url + path_str
        self.param_in = None

        self.should_generate = False
        self.http_method = None

        self.filename = replace_slash(remove_brackets(path_str))

        # Classname for the dataclass should be created from schema name
        # Nor from the filename since schemas can be reused and tracked better
        self.classname = capitalize_first_letter(self.filename[1:])

        self.set_param_in()
        self.generate_imports()

    def set_param_in(self):
        for operation in self.path:

            if operation == "get":  # No need to check for other http methods
                self.should_generate = True
                self.http_method = operation

                open_api_parameters = self.path[operation].get(
                    "parameters")

                print("path:", self.path_str.upper(), "\t\thttp:", operation,
                      "\t\tGenerate?:", self.should_generate)
                print("operation:",
                      self.path[operation])

                for param in open_api_parameters:
                    self.param_in = param.get("in")
            else:
                self.should_generate = False

    def generate_code(self):
        if self.should_generate:
            code = f"{self.imports}\n"
            code += f'url = "{self.url}"\n'
            code += f'params_in = "{self.param_in}"\n\n'
            code += f"client = RequestClass(url, params_in)\n"
            code += "client.make_request()\n"
            code += "ui.update()\n"

            return code

        return None

    def generate_imports(self):
        code = "from src.core.generators.open_api.generator.request_class import RequestClass\n"
        code += "from src.core.ui import ui\n"
        code += f'from src.generated_code.models.{self.filename} import {self.classname}\n'
        self.imports = code
