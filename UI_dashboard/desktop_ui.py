import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import asyncio
import threading
from typing import Dict, Any
import random
import datetime

from packages.identifier.identfier import create_identifier
from packages.recieve_spec_package.update import OpenAPIHandlerAPI


def find_first_numeric_property(schema: Dict[str, Any]) -> str:
    for prop, definition in schema.get("properties", {}).items():
        if definition.get("type") in ["number", "integer"]:
            return prop
    return None


class MonitoringUIDesktop:
    def __init__(self, handler: OpenAPIHandlerAPI):
        self.handler = handler
        self.specs: Dict[str, Dict[str, Any]] = {}

        self.root = tk.Tk()
        self.root.title("Monitoring UI")

        self.spec_selector = ttk.Combobox(self.root, state="readonly")
        self.spec_selector.pack(pady=10)

        self.plot_button = tk.Button(self.root, text="Plot selected spec",
                                     command=self.plot_selected)
        self.plot_button.pack(pady=10)

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Start listening for specs in a background thread
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._start_async_listener,
                         daemon=True).start()

    def _start_async_listener(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.listen_for_specs())

    async def listen_for_specs(self):
        while True:
            spec = await self.handler.wait_for_spec()
            self.process_spec(spec)

    def process_spec(self, spec: dict):
        paths = spec.get("paths", {})
        updated = False
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
                    updated = True

        if updated:
            self.spec_selector["values"] = list(self.specs.keys())
            if not self.spec_selector.get():
                self.spec_selector.current(0)

    def plot_selected(self):
        identifier = self.spec_selector.get()
        if not identifier or identifier not in self.specs:
            return

        y_key = self.specs[identifier]["y_key"]
        timestamps = [datetime.datetime.now() + datetime.timedelta(minutes=i)
                      for i in range(10)]
        values = [random.uniform(20, 30) for _ in range(10)]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(timestamps, values)
        ax.set_title(identifier)
        ax.set_xlabel("Time")
        ax.set_ylabel(y_key)

        self.canvas.draw()

    def run(self):
        self.root.mainloop()
