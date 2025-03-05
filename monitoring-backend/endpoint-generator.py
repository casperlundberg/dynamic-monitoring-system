# Description: This file contains the
# code for generating the endpoint from
# the paths obj. The generated endpoint should
# be python code that can be used to create
# the endpoint in the monitoring-backend.
import helper_functions as hf

# @param path_obj: Eg "/pet": {...}
# @param path: Eg "/pet"
def generate_endpoint(path_obj, path):
    paths = hf.load_paths()
    path_id = hf.get_new_id(paths, path)

    methods = list(path_obj.keys())

    function_name = path.replace("/", "").replace("{", "").replace("}", "").replace("-", "_")
    function_name = f"{function_name}_{path_id}"

    path = f"{path}_{path_id}"

    paths = hf.prep_paths_for_save(paths, path, path_id)
    hf.save_paths(paths)

    endpoint = f"""
    @app.route('{path}', methods={methods})
    def {function_name}():
    
        response = get_response('{path}')
        return response
    """
    print(endpoint)
