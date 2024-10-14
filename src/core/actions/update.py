"""
terminal input that receives a POST request with a JSON body containing an IDL document
which will be either OpenAPI or AsyncAPI. It will call for the generation
of code that can interact with the API described in the IDL document.
"""
import json
import os
import yaml
import requests


def update():
    idl = load_idl_document()  # returns IDL as a python dict

    print(idl)

    if idl is None:
        return
    # check if the idl is openapi or asyncapi
    # if idl["openapi"]:
    #     # TODO: call the openapi code generator
    # elif idl["asyncapi"]:
    #     # TODO: call the asyncapi code generator


def load_idl_document():
    """
    Load the IDL document from the terminal input
    """
    idl_path = input("Enter the IDL path: ")

    # check if the path is an url or a file path
    if idl_path.startswith("http"):
        return load_idl_document_from_url(idl_path)
    else:
        return load_idl_document_from_filepath(idl_path)


def load_idl_document_from_filepath(file_path):
    # check if the file is valid
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


# playtest - remove before deployment
update()
