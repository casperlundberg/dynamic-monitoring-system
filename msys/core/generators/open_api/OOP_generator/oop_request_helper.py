import requests


class RequestHelper:
    def __init__(self, http_obj):
        """
        Helper class to make requests to the server
        :param http_obj: an instance of HTTPModel
        """
        self.path_params = http_obj.path_params or {}
        self.request_args = http_obj.request_args or {}
        self.url = http_obj.SERVER + http_obj.PATH or http_obj.url
        self.response = None
        self.metrics = None

    def set_path_params(self, params):
        self.path_params = params

    def set_query_params(self, params):
        self.request_args['params'] = params

    def set_header_params(self, params):
        if params:
            self.request_args['headers'] = params

    def set_cookie_params(self, params):
        if params:
            self.request_args['cookies'] = params

    def set_request_args(self, params):
        self.request_args = params

    def make_request(self):
        self.url = self.replace_placeholders(self.url)

        if self.request_args:
            self.response = requests.get(self.url, **self.request_args)
        else:
            self.response = requests.get(self.url)

        self.metrics = {
            "response_time_ms": self.response.elapsed.total_seconds() * 1000,
            "status_code": self.response.status_code,
            "content_type": self.response.headers.get("Content-Type", ""),
            "content_length": self.response.headers.get("Content-Length", ""),
        }

    def replace_placeholders(self, url: str) -> str:
        for key, value in self.path_params.items():
            url = url.replace(f"{{{key}}}", str(value))
        return url
