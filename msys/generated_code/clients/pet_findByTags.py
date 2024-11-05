class PetFindByTags:
    def __init__(self):
        self.SERVER = "https://petstore3.swagger.io/api/v3"
        self.PATH = "/pet/findByTags"
        self.path_params = {}
        self.request_args = {}
        
        self.url = self.SERVER + self.PATH
        self.response = None
        self.metrics = {}
        