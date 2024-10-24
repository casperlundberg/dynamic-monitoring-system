class OOPGenerator:
    def __init__(self, spec: dict):
        self.spec = spec
        self.files = []

    def generate_code_file_obj(self):
        paths = self.spec.get("paths")
        for path in paths:
            path_str = str(path)
            path_obj = paths[path]
            server_url = self.spec.get("servers")[0].get("url")
            file_gen = ClientFileGenerator(path_obj, path_str, server_url)

            self.files.append(file_gen)

    def generate_code(self):
        for file in self.files:
            file.generate_code()


class ClientFileGenerator:
    def __init__(self, path: dict, path_str, server_url: str):
        self.path = path
        self.path_str = path_str
        self.server_url = server_url
        self.imports = None
        self.url = server_url + path_str

        self.path_params = None

        self.should_generate = False
        self.http_method = None

        self.filename = None

        # Classname for the dataclass should be created from schema name
        # Nor from the filename since schemas can be reused and tracked better
        self.classname = None

        self.code_string = ""

        self.parse_path_params()
        self.parse_filename()
        self.parse_classname()

    def parse_path_params(self):
        # get the path parameters inside {}
        self.path_params = {part.split("}")[0]: 0 for part in
                            self.path_str.split("{")[1:]}

    def parse_filename(self):
        filename = self.path_str.replace("/", "_")
        self.filename = filename.replace("{", "").replace("}", "")[1:]

    def parse_classname(self):
        # classname = self.filename[0].upper() + self.filename[1:]
        classname = self.filename
        classname = classname[0].upper() + classname[1:]

        # Upper case the first letter after each underscore
        for i in range(len(classname)):
            if classname[i] == "_":
                classname = (classname[:i + 1]
                             + classname[i + 1].upper()
                             + classname[i + 2:])

        classname = classname.replace("_", "")
        self.classname = classname

    def generate_code(self):
        self_server_var_name = "self.SERVER"
        self_path_var_name = "self.PATH"
        
        self.code_string = f"""class {self.classname}:
    def __init__(self):
        {self_server_var_name} = "{self.server_url}"
        {self_path_var_name} = "{self.path_str}"
        self.path_params = {self.path_params}
        self.request_args = {{}}
        
        self.url = {self_server_var_name} + {self_path_var_name}
        self.response = None
        self.metrics = {{}}
        """
