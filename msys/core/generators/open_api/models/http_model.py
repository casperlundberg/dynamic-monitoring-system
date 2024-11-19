from dataclasses import dataclass
from typing import List, Any


@dataclass
class HistoricalData:
    body: Any  # This is the response body
    metrics: dict  # This is the metrics of the response
    timestamp: str  # This is the timestamp of the response as a date string


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
    http_method: str  # "GET" or "OPTIONS"

    response_type: str  # "list" or "Single"
    response_body: dict
    metrics: dict

    x_axis: str  # This is a string that represents the x-axis choice
    y_axis: str  # This is a string that represents the y-axis choice

    # This is the historical data that is used for plotting
    # The historical data is a list of responses
    # Each response is a dictionary with the response body, metrics and timestamp
    # Use this instead of response_body and metrics to plot when
    # the body does not contain lists of objects
    historical_data: List[HistoricalData]

    # These are the specs for the parameters, response and components
    # Should be handled before reaching this class and pass processed data
    # to be used here, that is a better design.
    parameters_spec: dict
    response_spec: dict
    components_spec: dict
