# takes an Openapi schema and generates an endpoint that handles each root level data obj (http body)
# as the data that can be requested, as an array of such objects. This means that for every type of http body,
# one can request a time-series data representation of it.

class EndpointGenerator:
    def __init__(self):
        pass

    def parse_paths_obj(self, paths_obj):
        endpoints = []
        for path in paths_obj:
            endpoint = Endpoint(path)
            endpoints.append(endpoint)


class Endpoint:
    def __init__(self, path):
        self.path = path
        self.query_params

    def

