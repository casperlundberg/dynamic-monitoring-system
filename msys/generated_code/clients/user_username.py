class UserUsername:
    def __init__(self):
        self.SERVER = "https://petstore3.swagger.io/api/v3"
        self.PATH = "/user/{username}"
        self.path_params = {'username': 0}
        self.request_args = {}
        
        self.url = self.SERVER + self.PATH
        self.response = None
        self.metrics = {}
        