import requests


def replace_placeholders(url: str, values: dict) -> str:
    for key, value in values.items():
        url = url.replace(f"{{{key}}}", str(value))
    return url


def replace_parameters_in_query(url: str, parameters: dict) -> str:
    if "?" in url:
        base_url, query_string = url.split("?", 1)
        query_params = query_string.split("&")
        updated_params = []
        for param in query_params:
            key, value = param.split("=")
            if key in parameters:
                value = parameters[key]
            updated_params.append(f"{key}={value}")
        return f"{base_url}?" + "&".join(updated_params)
    return url


class RequestClass:
    def __init__(self, url, params_in):
        self.url = url
        self.params_in = params_in
        self.response = None
        self.body = None
        self.metrics = {}

    def change_param_in_url(self, params):
        if self.params_in == "path":
            self.url = replace_placeholders(self.url, params)
        elif self.params_in == "query":
            self.url = replace_parameters_in_query(self.url, params)
        else:
            raise ValueError("No parameters to replace")

    def make_request(self):
        self.response = requests.get(self.url)
        self.body = self.response.json()
        self.metrics = {
            "response_time": self.response.elapsed.total_seconds(),
            "status_code": self.response.status_code,
            "content_type": self.response.headers["Content-Type"],
            "content_length": self.response.headers["Content-Length"],
        }
