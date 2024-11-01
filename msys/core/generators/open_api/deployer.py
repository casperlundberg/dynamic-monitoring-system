import os
import pickle

from deifinitions import ROOT_DIR, GENERATED_CODE_FOLDER, \
    GENERATED_CODE_CLIENT_FOLDER, GENERATED_CODE_MODEL_FOLDER, MSYS_FOLDER, \
    GENERATED_CODE_SAVED_CLIENTS_FOLDER, GENERATED_CODE_SAVED_MODELS_FOLDER, \
    SAVED_OBJECTS_FOLDER


class Deployer:
    def __init__(self, generator):
        """
        Deploy the generated code to the specified locations
        :param generator: the generator in use
        """
        self.client_files = generator.client_files
        self.model_files = generator.model_files

    def deploy_models(self):
        # Deploy the code to the specified locations
        for file in self.model_files:
            model_code = file.code_string
            generated_code_folder_path = self.get_deploy_path()

            self.create_model_file(file.filename,
                                   generated_code_folder_path, model_code)

    def deploy_clients(self):
        # Deploy the code to the specified locations
        for file in self.client_files:
            client_code = file.code_string
            generated_code_folder_path = self.get_deploy_path()

            self.create_client_file(file.filename,
                                    generated_code_folder_path, client_code)
            self.save_client_file_obj(file, generated_code_folder_path)

    def get_deploy_path(self):
        # Get the path to deploy the code to
        path = os.path.join(ROOT_DIR, MSYS_FOLDER, GENERATED_CODE_FOLDER)
        return path

    def create_model_file(self, model_file_name, deploy_path,
                          model_code):
        # Create the model file
        file_path = os.path.join(deploy_path, GENERATED_CODE_MODEL_FOLDER,
                                 f"{model_file_name}.py")
        if model_code is not None:
            with open(file_path, "w") as f:
                f.write(model_code)

    def create_client_file(self, client_file_name, deploy_path,
                           client_code):
        # Create the client file
        file_path = os.path.join(deploy_path, GENERATED_CODE_CLIENT_FOLDER,
                                 f"{client_file_name}.py")

        if client_code is not None:
            with open(file_path, "w") as f:
                f.write(client_code)

    def save_model_file_obj(self, model_file_obj, deploy_path):
        # Save the model file data
        file_path = os.path.join(deploy_path, SAVED_OBJECTS_FOLDER,
                                 GENERATED_CODE_SAVED_MODELS_FOLDER,
                                 f"{model_file_obj.filename}.pkl")
        with open(file_path, "wb") as f:
            pickle.dump(model_file_obj, f, pickle.HIGHEST_PROTOCOL)

    def save_client_file_obj(self, client_file_obj, deploy_path):
        # Save the client file data
        file_path = os.path.join(deploy_path, SAVED_OBJECTS_FOLDER,
                                 GENERATED_CODE_SAVED_CLIENTS_FOLDER,
                                 f"{client_file_obj.filename}.pkl")
        with open(file_path, "wb") as f:
            pickle.dump(client_file_obj, f, pickle.HIGHEST_PROTOCOL)

    def load_model_file_obj(self, filename, deploy_path):
        # Load the model file data
        file_path = os.path.join(deploy_path, SAVED_OBJECTS_FOLDER,
                                 GENERATED_CODE_SAVED_CLIENTS_FOLDER,
                                 f"{filename}.pkl")
        with open(file_path, "rb") as f:
            return pickle.load(f)

    def load_client_file_obj(self, filename, deploy_path):
        # Load the client file data
        file_path = os.path.join(deploy_path, SAVED_OBJECTS_FOLDER,
                                 GENERATED_CODE_SAVED_CLIENTS_FOLDER,
                                 f"{filename}.pkl")
        with open(file_path, "rb") as f:
            return pickle.load(f)

    def deploy(self):
        # Deploy the code
        self.deploy_models()
        self.deploy_clients()
