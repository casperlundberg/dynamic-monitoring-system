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

    response_body: dict
    metrics: dict

    x_axis: str  # This is a string that represents the x-axis choice
    y_axis: str  # This is a string that represents the y-axis choice

    # These are the specs for the parameters, response and components
    # Should be handled before reaching this class and pass processed data
    # to be used here, that is a better design.
    parameters_spec: dict
    response_spec: dict
    components_spec: dict
