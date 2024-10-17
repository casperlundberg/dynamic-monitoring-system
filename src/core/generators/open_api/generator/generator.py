class Generator:
    def __init__(self, spec: dict):
        self.spec = spec
        self.code = ""

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


class PathGenerator:
    def __init__(self, paths: dict):
        self.paths = paths
        self.imports = ""
        self.url = ""

    def generate(self):
        self.code += self.generate_request()
        self.code += self.generate_response()

    def generate_request(self):
        request = self.spec.get("paths").get(self.path).get("request")
        request_code = f'response = requests.{request.get("method")}('
        request_code += f'{self.generate_url()})\n'
        return request_code

    def generate_url(self):
        url = f'server_url + path_url + {self.generate_parameters()}'
        return url

    def generate_parameters(self):
        params = ""
        for param in self.spec.get("paths").get(self.path).get("parameters"):
            params += f'{param.get("name")}, '
        return params

    def generate_response(self):
        response = self.spec.get("paths").get(self.path).get("response")
        response_code = f'body = response.{response.get("method")}()\n'
        response_code += f'{self.generate_model()}'
        response_code += f'{self.generate_metrics()}'
        response_code += f'{self.generate_ui_update()}'
        return response_code

    def generate_model(self):
        model = self.spec.get("paths").get(self.path).get("model")
        model_code = f'{model.get("name")} = {model.get("class")}(**body)\n'
        return model_code

    def generate_metrics(self):
        metrics = self.spec.get("paths").get(self.path).get("metrics")
        metrics_code = "metrics = {\n"
        for metric in metrics:
            metrics_code += f'"{metric}": response.{metric},\n'
        metrics_code += "}\n"
        return metrics_code

    def generate_ui_update(self):
        ui_update = self.spec.get("paths").get(self.path).get("ui_update")
        ui_update_code = "ui.update_metrics(metrics)\n"
        ui_update_code += f'ui.update_{ui_update.get("model")}({ui_update.get("model")})\n'
        return ui_update_code
