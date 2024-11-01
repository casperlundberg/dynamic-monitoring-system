from dataclasses import dataclass


# Can be used instead of generated clients.
# That would mean that each instance of this class
# would be a request to the server.
# It also means that the instance would be meant to be pickled
# Then, the generator do not generate code for clients but instead generate
# the data needed to create an instance of this class and a pickle file
@dataclass
class HTTPModel:
    SERVER: str
    PATH: str
    path_params: dict
    request_args: dict
    url: str
    parameters_spec: dict
