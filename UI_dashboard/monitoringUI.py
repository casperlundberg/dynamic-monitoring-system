import asyncio
import random
import datetime
import base64
from io import BytesIO
from typing import Dict, Any

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from matplotlib.figure import Figure

from packages.identifier.identfier import create_identifier
from packages.recieve_spec_package.update import OpenAPIHandlerAPI


def find_first_numeric_property(schema: Dict[str, Any]) -> str:
    for prop, definition in schema.get("properties", {}).items():
        if definition.get("type") in ["number", "integer"]:
            return prop
    return None


class MonitoringUI:
    def __init__(self, openapi_handler: OpenAPIHandlerAPI):
        self.openapi_handler = openapi_handler
        self.app = openapi_handler.app
        self.templates = Jinja2Templates(directory="templates")
        self.specs: Dict[
            str, Dict[str, Any]] = {}
        self.setup_ui_routes()

        # Start async background task
        # asyncio.create_task(self.listen_for_specs())

    def setup_ui_routes(self):
        @self.app.get("/panels/{identifier}", response_class=HTMLResponse)
        async def render_panel(request: Request, identifier: str):
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

            return self.templates.TemplateResponse("panel.html", {
                "request": request,
                "identifier": identifier,
                "y_key": y_key,
                "plot_img": img_base64
            })

    async def listen_for_specs(self):
        while True:
            spec = await self.openapi_handler.wait_for_spec()
            self.process_spec(spec)

    def process_spec(self, spec: dict):
        paths = spec.get("paths", {})
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                identifier = create_identifier(spec, path, method)

                response_schema = operation.get("responses", {}).get("200",
                                                                     {}).get(
                    "content", {}).get("application/json", {}).get("schema")
                if not response_schema or not isinstance(response_schema,
                                                         dict):
                    continue

                y_key = find_first_numeric_property(response_schema)
                if y_key:
                    self.specs[identifier] = {
                        "schema": response_schema,
                        "y_key": y_key
                    }
