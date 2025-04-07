import importlib.util
import os
import time
from flask import Flask, jsonify, request, Response
from threading import Thread

app = Flask(__name__)

loaded_blueprints = set()
blueprint_mod_times = {}
endpoint_handlers = {}


def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_blueprints():
    global loaded_blueprints, blueprint_mod_times, endpoint_handlers
    generated_endpoints_folder = os.path.join(os.path.dirname(__file__),
                                              '../generated_endpoints')

    current_blueprints = set()

    for filename in os.listdir(generated_endpoints_folder):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            file_path = os.path.join(generated_endpoints_folder, filename)
            mod_time = os.path.getmtime(file_path)

            current_blueprints.add(module_name)

            if module_name not in loaded_blueprints or blueprint_mod_times.get(
                    module_name) != mod_time:
                module = import_module_from_file(module_name, file_path)
                blueprint = f'blueprint_{module_name}'
                if hasattr(module, blueprint):
                    handler = getattr(module, f'handle_{module_name}', None)

                    if handler:
                        endpoint_handlers[
                            f'/{module_name.replace("_", "/")}'] = handler
                    loaded_blueprints.add(module_name)
                    blueprint_mod_times[module_name] = mod_time

    # Remove handlers for deleted endpoints
    deleted_blueprints = loaded_blueprints - current_blueprints
    for module_name in deleted_blueprints:
        endpoint_path = f'/{module_name.replace("_", "/")}'
        if endpoint_path in endpoint_handlers:
            del endpoint_handlers[endpoint_path]
        loaded_blueprints.remove(module_name)
        if module_name in blueprint_mod_times:
            del blueprint_mod_times[module_name]


def monitor_blueprints():
    while True:
        load_blueprints()
        time.sleep(10)  # Check for new blueprints every 10 seconds


# Preload all blueprints before the first request
load_blueprints()

# Start the background thread to monitor blueprints
thread = Thread(target=monitor_blueprints)
thread.daemon = True
thread.start()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    handler = endpoint_handlers.get(f'/{path}')

    if handler:
        return handler()
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
