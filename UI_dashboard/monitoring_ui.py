import asyncio
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import datetime
import threading

import definitions
from UI_dashboard.queue import update_event, shared_queue
from packages.identifier.identfier import create_identifier
from packages.recieve_spec_package.update import OpenAPIHandlerAPI
from packages.recieve_spec_package.deref_clean import clean_dereference


def find_first_numeric_property(schema):
    for prop, definition in schema.get("properties", {}).items():
        if definition.get("type") in ["number", "integer"]:
            return prop
    return None


class MonitoringUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.specs = {}

        self.panel_frame = tk.Frame()
        self.panel_frame.pack(fill="both", expand=True)

        self.plot_frame = tk.Frame()
        self.plot_frame.pack(fill="both", expand=True)

    def add_spec(self, identifier, y_key):
        self.specs[identifier] = {"y_key": y_key}
        self.refresh_ui()

    def check_for_updates(self):
        if update_event.is_set():
            spec = shared_queue.get()  # Get the generator object from the queue
            # Process the specification document
            self.process_spec(spec)
            update_event.clear()  # Clear the event

        self.after(100,
                   self.check_for_updates)  # Check for updates every 100ms

    def refresh_ui(self):
        for widget in self.panel_frame.winfo_children():
            widget.destroy()

        for identifier in self.specs:
            btn = tk.Button(self.panel_frame, text=identifier,
                            command=lambda i=identifier: self.show_plot(i))
            btn.pack(fill="x", pady=2)

    def show_plot(self, identifier):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        y_key = self.specs[identifier]["y_key"]
        timestamps = [datetime.datetime.now().replace(second=0,
                                                      microsecond=0) + datetime.timedelta(
            minutes=i) for i in range(10)]
        values = [random.uniform(20, 30) for _ in range(10)]

        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)
        ax.plot(timestamps, values)
        ax.set_title(identifier)
        ax.set_xlabel("Timestamp")
        ax.set_ylabel(y_key)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def process_spec(self, spec):
        for path, path_item in spec.get("paths", {}).items():
            for method, operation in path_item.items():
                identifier = create_identifier(spec, path, method)
                response_schema = operation.get("responses", {}).get("200",
                                                                     {}).get(
                    "content", {}).get("application/json", {}).get("schema")
                if not response_schema:
                    continue
                y_key = find_first_numeric_property(response_schema)
                if y_key:
                    print(f"[UI] Adding: {identifier} with y-axis: {y_key}")
                    self.add_spec(identifier, y_key)
