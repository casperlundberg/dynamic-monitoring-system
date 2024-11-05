class V1Forecast:
    def __init__(self):
        self.SERVER = "https://api.open-meteo.com"
        self.PATH = "/v1/forecast"
        self.path_params = {}
        self.request_args = {}
        
        self.url = self.SERVER + self.PATH
        self.response = None
        self.metrics = {}
        