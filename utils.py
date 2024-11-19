import os
import pickle

from matplotlib import pyplot as plt

from deifinitions import ROOT_DIR, GENERATED_CODE_FOLDER, MSYS_FOLDER, \
    SAVED_OBJECTS_FOLDER, GENERATED_CODE_SAVED_CLIENTS_FOLDER
from msys.core.generators.open_api.models.http_model import HistoricalData


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


def is_array_nested(data):
    """
    Check if there is an array somewhere nested in the data
    """
    if isinstance(data, list):
        return True
    for k, v in data.items():
        if isinstance(v, dict):
            return is_array_nested(v)
        elif isinstance(v, list):
            return True
    return False


# data1 = {
#     "name": "John",
#     "age": 30,
#     "cars": {
#         "car1": "Ford",
#         "car2": "BMW",
#         "car3": ["Ford", "BMW"]
#     }
# }
# print(is_array_nested(data1))


def is_key_array_or_nested_deeper(data, key):
    """
    Check if the key is an array or nested deeper in the data
    """
    keys = key.split('.')
    array_found = False
    for k in keys:
        if isinstance(data, dict):
            data = data.get(k)
        elif isinstance(data, list):
            data = [item.get(k) for item in data if isinstance(item, dict)]
        if isinstance(data, list):
            array_found = True
    return array_found


# data1 = {
#     "name": "John",
#     "age": 30,
#     "cars": {
#         "car1": "Ford",
#         "car2": "BMW",
#         "list": [
#             {
#                 "brand": {
#                     "name": "Chevrolet",
#                 }
#             },
#             "BMW"]
#     }
# }
# print(is_key_array_or_nested_deeper(data1, "cars"))
# print(is_key_array_or_nested_deeper(data1, "cars.list"))
# print(is_key_array_or_nested_deeper(data1, "cars.list.brand"))
# print(is_key_array_or_nested_deeper(data1, "cars.list.brand.name"))


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


# Test find_value_by_key function for list of dictionaries

# car1 = {
#     "brand": {
#         "name": "Chevrolet",
#         "model": "Impala"
#     },
#     "year": 1964
# }
#
# car2 = {
#     "brand": {
#         "name": "Ford",
#         "model": "Mustang"
#     },
#     "year": 2008
# }
#
# car3 = {
#     "brand": {
#         "name": "BMW",
#         "model": "X5"
#     },
#     "year": 2018
# }
#
# body = {
#     "cars": [car1, car2, car3]
# }
#
# print(find_value_by_key(body, "cars.brand.name"))
# print(find_value_by_key(body, "cars.brand.model"))
# print(find_value_by_key(body, "cars.year"))

# array_body = [
#     {
#         "data": {
#             "test": 1
#         }
#     },
#     {
#         "data": {
#             "test": 3
#         }
#     }
# ]
#
# print(find_value_by_key(array_body, "data.test"))

def find_history_data_by_key(data_list, key):
    """
    Find historical data by key
    @Param data_list: List of HistoricalData objects
    @Param key: Key to search in the HistoricalData objects
    @Return: List of values found by the key
    """
    result = []
    for data in data_list:
        dict_ = data.__dict__
        value = find_value_by_key(dict_, key)
        if value is not None:
            result.append(value)
    return result

# d1 = {
#     "body": {
#         "name": "John",
#         "age": 30
#     },
#     "metrics": {
#         "response_time_ms": 100,
#         "status_code": 200
#     },
#     "timestamp": 1000
# }
#
# d2 = {
#     "body": {
#         "name": "John",
#         "age": 11
#     },
#     "metrics": {
#         "response_time_ms": 2,
#         "status_code": 200
#     },
#     "timestamp": 23
# }
#
# h1 = HistoricalData(**d1)
# h2 = HistoricalData(**d2)
# data_li = [h1, h2]
# print(find_history_data_by_key(data_li, "metrics.response_time_ms"))
# print(find_history_data_by_key(data_li, "body.age"))

# lst = [HistoricalData(
#     body={'id': 5, 'category': {'id': 1, 'name': 'Dogs'}, 'name': 'Dog 2',
#           'photoUrls': ['url1', 'url2'],
#           'tags': [{'id': 1, 'name': 'tag2'}, {'id': 2, 'name': 'tag3'}],
#           'status': 'sold'},
#     metrics={'response_time_ms': 768.2560000000001, 'status_code': 200,
#              'content_type': 'application/json', 'content_length': '156'},
#     timestamp='2024-11-19 12:22:32'), HistoricalData(
#     body={'id': 5, 'category': {'id': 1, 'name': 'Dogs'}, 'name': 'Dog 2',
#           'photoUrls': ['url1', 'url2'],
#           'tags': [{'id': 1, 'name': 'tag2'}, {'id': 2, 'name': 'tag3'}],
#           'status': 'sold'},
#     metrics={'response_time_ms': 25, 'status_code': 200,
#              'content_type': 'application/json', 'content_length': '156'},
#     timestamp='2024-11-19 12:30:00')]
# x_field = "timestamp"
# y_field = "body.id"
# x_data = find_history_data_by_key(lst, x_field)
# y_data = find_history_data_by_key(lst, y_field)
# print(x_data)
# print(y_data)

# fig, ax = plt.subplots(figsize=(10, 6))
# ax.plot(x_data, y_data, marker='o')
# ax.set_xlabel(x_field)
# ax.set_ylabel(y_field)
# ax.set_title(f"{x_field} vs {y_field}")
# plt.show()
