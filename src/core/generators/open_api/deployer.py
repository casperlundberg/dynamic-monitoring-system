import os
from src.deifinitions import ROOT_DIR, GENERATED_CODE_FOLDER, \
    GENERATED_CODE_CLIENT_FOLDER, GENERATED_CODE_MODEL_FOLDER, \
    GENERATED_CODE_UI_FOLDER


class Deployer:
    def __init__(self, generator):
        """
        Deploy the generated code to the specified locations
        :param generator: the generator in use
        """
        self.client_files = generator.client_files
        self.generated_code_folder = GENERATED_CODE_FOLDER
        self.client_folder = GENERATED_CODE_CLIENT_FOLDER
        self.model_folder = GENERATED_CODE_MODEL_FOLDER

    def deploy_clients(self):
        # Deploy the code to the specified locations
        for file in self.client_files:
            client_code = file.code_string
            generated_code_folder_path = self.get_deploy_path()

            self.create_client_file(file.filename,
                                    generated_code_folder_path, client_code)

    def get_deploy_path(self):
        # Get the path to deploy the code to
        path = os.path.join(ROOT_DIR, self.generated_code_folder)
        return path

    def create_model_file(self, model_file_name, path,
                          model_code):
        # Create the model file
        file_path = os.path.join(path, self.model_folder,
                                 f"{model_file_name}.py")
        if model_code is not None:
            with open(file_path, "w") as f:
                f.write(model_code)

    def create_client_file(self, client_file_name, path,
                           client_code):
        # Create the client file
        file_path = os.path.join(path, self.client_folder,
                                 f"{client_file_name}.py")

        if client_code is not None:
            with open(file_path, "w") as f:
                f.write(client_code)
