import json
import os
import yaml
import requests
from src.core.generators.open_api.generator.generator import Generator
from src.core.generators.open_api.deployer import Deployer


def update(input):
    """
    Update the codebase based on the IDL document
    :return:
    """
    idl = load_idl_document(input)  # returns IDL as a python dict

    if idl is None:
        return

    if idl["openapi"]:
        code_gen = Generator(idl)
        code_gen.generate()
        deployer = Deployer(code_gen.files)
        deployer.deploy()

    elif idl["asyncapi"]:
        print("AsyncAPI")
        # TODO: call the asyncapi code generator


def load_idl_document(input):
    """
    Load the IDL document from the terminal input
    :return: IDL as a python dict
    """
    if input:
        idl_path = input
    else:
        idl_path = input("Enter the IDL path: ")

    # check if the path is an url or a file path
    if idl_path.startswith("http"):
        return load_idl_document_from_url(idl_path)
    else:
        return load_idl_document_from_filepath(idl_path)


def load_idl_document_from_filepath(file_path):
    """
    Load the IDL document from a file path
    :param file_path:
    :return: IDL as a python dict
    """
    if not os.path.isfile(file_path):
        print("Invalid file path")
        return

    # check the file type
    if file_path.endswith(".yaml") or file_path.endswith(".yml"):
        # yml to python dict
        return yaml.load(open(file_path, 'r'), Loader=yaml.FullLoader)
    elif file_path.endswith(".json"):
        # json to python dict
        return json.load(open(file_path, 'r'))
    else:
        print("Invalid file type")
        return


def load_idl_document_from_url(url):
    """
    Load the IDL document from a URL
    :param url: URL of the raw IDL document
    :return: IDL as a python dict
    """
    response = requests.get(url, allow_redirects=True)
    content = response.content.decode("utf-8")

    if response.status_code != 200:
        print("Invalid URL")
        return

    if not (content.startswith("{") or content.startswith(
            "openapi") or content.startswith("asyncapi")):
        print("Invalid IDL document")
        return

    # check the file type
    if url.endswith(".yaml") or url.endswith(".yml"):
        return yaml.load(content, Loader=yaml.FullLoader)
    elif url.endswith(".json"):
        return json.loads(content)
    else:
        print("Invalid file type")
        return


update("C:/Users/Desktop-Lumpa/Downloads/openapi.json")
