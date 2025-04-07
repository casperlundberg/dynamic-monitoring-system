import json
import hashlib
import yaml
import random
import datetime
import jsonref

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from typing import Dict, Any
from matplotlib.figure import Figure
from io import BytesIO
import base64

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from packages.recieve_spec_package.update import OpenAPIHandlerAPI


# --- IDENTIFIER LOGIC ---
def generate_hash(spec: Dict[str, Any]) -> str:
    spec_str = json.dumps(spec, sort_keys=True)
    return hashlib.sha256(spec_str.encode('utf-8')).hexdigest()


def create_identifier(spec: Dict[str, Any], path: str, method: str) -> str:
    hash_value = generate_hash(spec)
    return f"{method.lower()}{path.replace('/', '_').replace('{', '').replace('}', '')}_{hash_value}"


def find_first_numeric_property(schema: Dict[str, Any]) -> str:
    for prop, definition in schema.get("properties", {}).items():
        if definition.get("type") in ["number", "integer"]:
            return prop
    return None


# --- UI EXTENSION FOR OpenAPIHandlerAPI ---
class MonitoringUI:
    def __init__(self, openapi_handler: OpenAPIHandlerAPI):
        self.app = openapi_handler
        self.openapi_handler = openapi_handler
        self.templates = Jinja2Templates(directory="templates")
        self.specs = {}  # identifier -> schema mapping
        self.setup_ui_routes()

    def setup_ui_routes(self):
        @self.app.get("/panels/{identifier}", response_class=HTMLResponse)
        async def render_panel(request: Request, identifier: str):
            spec = self.openapi_handler.get_spec()
            if spec is None:
                return HTMLResponse("<h1>No spec loaded</h1>", status_code=404)

            if identifier not in self.specs:
                # Reprocess the spec to populate self.specs
                self.process_spec(spec)

            if identifier not in self.specs:
                return HTMLResponse("<h1>Identifier not found</h1>",
                                    status_code=404)

            y_key = self.specs[identifier]["y_key"]
            timestamps = [datetime.datetime.now().replace(second=0,
                                                          microsecond=0) + datetime.timedelta(
                minutes=i) for i in range(10)]
            values = [random.uniform(20, 30) for _ in range(10)]

            fig = Figure()
            ax = fig.subplots()
            ax.plot(timestamps, values)
            ax.set_title(identifier)
            ax.set_xlabel("Timestamp")
            ax.set_ylabel(y_key)

            buf = BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode("utf-8")

            return self.templates.TemplateResponse("panel.html",
                                                   {"request": request,
                                                    "identifier": identifier,
                                                    "y_key": y_key,
                                                    "plot_img": img_base64})

    def process_spec(self, spec: dict):
        paths = spec.get("paths", {})
        schemas = spec.get("components", {}).get("schemas", {})

        for path, path_item in paths.items():
            for method, operation in path_item.items():
                identifier = create_identifier(spec, path, method)
                response_ref = operation.get("responses", {}).get("200",
                                                                  {}).get(
                    "content", {}).get("application/json", {}).get("schema",
                                                                   {}).get(
                    "$ref", "")
                schema_name = response_ref.split("/")[
                    -1] if response_ref else None
                schema = schemas.get(schema_name) if schema_name else None

                if schema:
                    y_key = find_first_numeric_property(schema)
                    if y_key:
                        self.specs[identifier] = {
                            "schema": schema,
                            "y_key": y_key
                        }


# --- BUILD APP ---
from packages.recieve_spec_package.update import OpenAPIHandlerAPI

openapi_handler = OpenAPIHandlerAPI()
monitoring_ui = MonitoringUI(openapi_handler)
app = monitoring_ui.app
app.mount("/static", StaticFiles(directory="static"), name="static")
