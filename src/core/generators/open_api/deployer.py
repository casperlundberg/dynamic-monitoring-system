import os
from src.deifinitions import ROOT_DIR


class Deployer:
    def __init__(self, files: list):
        # self.config = config
        self.files = files

    def deploy(self):
        # Deploy the code to the specified locations
        for file in self.files:
            client_code = file.generate_code()
            generated_code_folder_path = self.get_deploy_path()

            self.create_client_file(file.filename,
                                    generated_code_folder_path, client_code)

    def get_deploy_path(self):
        # Get the path to deploy the code to
        path = os.path.join(ROOT_DIR, "generated_code")
        return path

    def create_model_file(self, model_file_name, path,
                          model_code):
        # Create the model file
        with open(os.path.join(path, "models", f"{model_file_name}.py"),
                  "w") as f:
            f.write(model_code)

    def create_client_file(self, client_file_name, path,
                           client_code):
        # Create the client file
        file_path = os.path.join(path, "clients", f"{client_file_name}.py")
        print(file_path)
        
        if client_code is not None:
            with open(file_path, "w") as f:
                f.write(client_code)
