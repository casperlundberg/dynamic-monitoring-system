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
        self.classname = self.filename[0].upper() + self.filename[1:]

    def generate_code(self):
        self_server_var_name = "self.SERVER"
        self_path_var_name = "self.PATH"
        self.code_string = f"""
import requests


class {self.classname}:
    def __init__(self):
        {self_server_var_name} = "{self.server_url}"
        {self_path_var_name} = "{self.path_str}"
        self.path_params = {self.path_params}
        self.request_args = {{}}
        self.url = {self_server_var_name} + {self_path_var_name}
        
        self.response = None
        self.metrics = {{}}
        
    def set_path_params(self, params):
        self.path_params = params
        
    def set_query_params(self, params):
        self.request_args['params'] = params
        
    def set_header_params(self, params):
        self.request_args['headers'] = params
    
    def set_cookie_params(self, params):
        self.request_args['cookies'] = params
    
    def make_request(self):
        self.url = self.replace_placeholders(self.url)
        
        if self.request_args:
            self.response = requests.get(self.url, **self.request_args)
        else:
            self.response = requests.get(self.url)
        
        self.metrics = {{
            "response_time": self.response.elapsed.total_seconds(),
            "status_code": self.response.status_code,
            "content_type": self.response.headers["Content-Type"],
            "content_length": self.response.headers["Content-Length"],
        }}
        
    def replace_placeholders(self, url: str) -> str:
        for key, value in self.path_params.items():
            url = url.replace(f"{{{{key}}}}", str(value))
        return url
        """
