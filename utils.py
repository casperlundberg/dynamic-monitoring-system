import os
import pickle

from deifinitions import ROOT_DIR, GENERATED_CODE_FOLDER, MSYS_FOLDER, \
    SAVED_OBJECTS_FOLDER, GENERATED_CODE_SAVED_CLIENTS_FOLDER


def parse_server_variables(servers_obj):
    server_variables = []
    for server in servers_obj:
        var = server.get("variables")
        if var is not None:
            server_variables.append(var)
    return server_variables


def replace_server_variables(server_url, server_variables):
    for variable in server_variables:
        server_url = server_url.replace(f"{{{variable}}}",
                                        server_variables[variable])
    return server_url


def parse_server_urls(servers_obj):
    server_urls = []
    server_variables = parse_server_variables(servers_obj)
    for server in servers_obj:
        url = server.get("url")

        if not url.startswith("http"):
            raise ValueError(
                "Invalid URL, must be full URL. Current URL: " + url)

        if len(server_variables) > 0:
            parsed_url = replace_server_variables(url, server_variables)
        else:
            parsed_url = url

        server_urls.append(parsed_url)
    return server_urls


def generated_folder():
    return os.path.join(ROOT_DIR, MSYS_FOLDER, GENERATED_CODE_FOLDER)


def save_client_file_obj(http_obj, filename, deploy_path=None):
    # Save the client file data
    if deploy_path is None:
        deploy_path = generated_folder()

    if filename is None:
        raise ValueError("Filename cannot be None")

    file_path = os.path.join(deploy_path, SAVED_OBJECTS_FOLDER,
                             GENERATED_CODE_SAVED_CLIENTS_FOLDER,
                             f"{filename}.pkl")
    with open(file_path, "wb") as f:
        pickle.dump(http_obj, f, pickle.HIGHEST_PROTOCOL)


def load_client_file_obj(filename, deploy_path=None):
    # Check if filename is provided
    if not filename:
        raise ValueError("Filename cannot be None or empty")

    # Set deploy_path to generated_folder if not provided
    if deploy_path is None:
        deploy_path = generated_folder()

    # Construct the file path
    file_path = os.path.join(deploy_path, SAVED_OBJECTS_FOLDER,
                             GENERATED_CODE_SAVED_CLIENTS_FOLDER,
                             f"{filename}.pkl")

    # Check if the file exists
    if not os.path.exists(file_path):
        # raise FileNotFoundError(f"File not found: {file_path}")
        return None
    # Load the client file data
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except (pickle.PickleError, EOFError) as e:
        raise RuntimeError(f"Error loading pickle file: {e}")


def nested_dict_keys_to_list(d):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from nested_dict_keys_to_list(v)
        else:
            yield k


def nested_dict_get_value(d, key):
    for k, v in d.items():
        if k == key:
            return v
        if isinstance(v, dict):
            return nested_dict_get_value(v, key)


def find_value_by_key(data, key):
    """
    Recursively search through the response body to find the value for the given key
    """
    keys = key.split('.')
    for k in keys:
        if isinstance(data, dict):
            data = data.get(k)
        elif isinstance(data, list):
            data = [item.get(k) for item in data if isinstance(item, dict)]
        else:
            return None
    return data
