from msys.core.generators.open_api.models.http_model import HTTPModel
from msys.core.generators.open_api.OOP_generator.parser_functions import \
    parse_server_urls


class OOPGenerator:
    def __init__(self, spec: dict):
        self.spec = spec
        self.http_data_objs = {}

    def generate_client_file_obj(self):
        paths = self.spec.get("paths")
        if paths is None:
            return

        server_url = None
        # If global server, use that
        if self.spec.get("servers") is not None:
            server_obj = self.spec.get("servers")
            server_url = parse_server_urls(server_obj)[0]

        for path in paths:
            path_obj = paths[path]
            self.generate_http_obj(path, path_obj, server_url)

    def generate_http_obj(self, path, path_obj, server_url):

        # Path Server obj overrides the global server URL
        if path_obj.get("servers") is not None:
            server_obj = path_obj.get("servers")
            server_url = parse_server_urls(server_obj)[0]

        parameters_obj = None
        response_obj = None
        if path_obj.get("get") is not None:
            http_method = "GET"
            parameters_obj = path_obj.get("get").get("parameters")
            response_obj = path_obj.get("get").get("responses")
        else:
            http_method = "OPTIONS"
            # test all methods to get the parameters and response
            for method in path_obj:
                if method != "servers":
                    http_method = method
                    parameters_obj = path_obj.get(method).get("parameters")
                    response_obj = path_obj.get(method).get("responses")
                    break

        path_str = str(path)
        # path params should be fetched from the parameters obj
        # along with query, header, cookie params
        path_params = {part.split("}")[0]: 0 for part in
                       path_str.split("{")[1:]}
        url = server_url + path_str

        components_obj = self.spec.get("components")

        # fix response_type to be fetched from schema as if a list is found
        # it is a list of objects, otherwise it is a single object
        # Behave differently in the ui based on this.
        # This maybe belongs to the ui, so it can choose how to display the data
        # based on the type of the response and which
        # values that is chosen as x and y-axis

        http_obj = HTTPModel(SERVER=server_url, PATH=path_str,
                             path_params=path_params,
                             request_args={}, url=url,
                             parameters_spec=parameters_obj,
                             response_spec=response_obj,
                             response_body={}, metrics={},
                             components_spec=components_obj,
                             x_axis="", y_axis="",
                             http_method=http_method,
                             response_type="", historical_data=[])

        filename = http_obj.PATH.replace("/", "_")[1:]
        self.http_data_objs[filename] = http_obj
