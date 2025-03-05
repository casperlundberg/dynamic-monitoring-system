import importlib.util
import os
import time
from flask import Flask, jsonify

app = Flask(__name__)

loaded_blueprints = set()
blueprint_mod_times = {}

def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_blueprints():
    global loaded_blueprints, blueprint_mod_times
    generated_endpoints_folder = os.path.join(os.path.dirname(__file__), 'generated_endpoints')

    for filename in os.listdir(generated_endpoints_folder):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            file_path = os.path.join(generated_endpoints_folder, filename)
            mod_time = os.path.getmtime(file_path)

            if module_name not in loaded_blueprints or blueprint_mod_times.get(module_name) != mod_time:
                module = import_module_from_file(module_name, file_path)
                blueprint = f'blueprint_{module_name}'
                if hasattr(module, blueprint):
                    app.register_blueprint(getattr(module, blueprint))
                    loaded_blueprints.add(module_name)
                    blueprint_mod_times[module_name] = mod_time

@app.before_request
def before_request():
    load_blueprints()

@app.route('/')
def home():
    routes = [f'<a href="{rule}">{rule}</a>' for rule in app.url_map.iter_rules()]
    return '<br>'.join(routes)

if __name__ == '__main__':
    app.run(debug=True)