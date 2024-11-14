import os
import pickle

from deifinitions import ROOT_DIR, GENERATED_CODE_FOLDER, MSYS_FOLDER, \
    SAVED_OBJECTS_FOLDER, GENERATED_CODE_SAVED_CLIENTS_FOLDER


def generated_folder():
    """
    Get the generated folder path
    """
    return os.path.join(ROOT_DIR, MSYS_FOLDER, GENERATED_CODE_FOLDER)


def serialize_save_file(http_obj, filename, deploy_path=None):
    """
    Save an object to the given filename
    """
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


def deserialize_save_file(filename, deploy_path=None):
    """
    Load an object from the given filename
    """
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
    """
    Convert nested dictionary keys to a list
    """
    for k, v in d.items():
        if isinstance(v, dict):
            yield from nested_dict_keys_to_list(v)
        else:
            yield k


def nested_dict_get_value(d, key):
    """
    Search through a nested dictionary to find the value for the given key
    """
    for k, v in d.items():
        if k == key:
            return v
        if isinstance(v, dict):
            return nested_dict_get_value(v, key)


def find_value_by_key(data, key):
    """
    Find a value in a dictionary from a key (ex: parent.child.child)
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
