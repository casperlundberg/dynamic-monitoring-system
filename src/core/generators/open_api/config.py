class Config:
    def __init__(self, config: dict):
        self.config = config

    def get(self, key: str):
        return self.config.get(key)
