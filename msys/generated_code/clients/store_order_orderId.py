class StoreOrderOrderId:
    def __init__(self):
        self.SERVER = "https://petstore3.swagger.io/api/v3"
        self.PATH = "/store/order/{orderId}"
        self.path_params = {'orderId': 0}
        self.request_args = {}
        
        self.url = self.SERVER + self.PATH
        self.response = None
        self.metrics = {}
        