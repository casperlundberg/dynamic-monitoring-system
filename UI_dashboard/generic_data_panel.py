import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk

from dateutil.parser import parse

import requests
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import definitions
from definitions import LEFT_PANEL_WIDTH
from packages.flatten_prop_schema.flatten_prop import flatten_properties


def create_text_with_scrollbar(parent, text_content, expand=True):
    """
    Create a text widget with a scrollbar
    """
    for widget in parent.winfo_children():
        widget.destroy()

    body_canvas = tk.Text(parent, wrap=tk.WORD)
    scrollbar = tk.Scrollbar(parent, command=body_canvas.yview)
    body_canvas.configure(yscrollcommand=scrollbar.set)

    body_canvas.insert(tk.END, text_content)
    body_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=expand)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


def identifier_to_url(identifier):
    """
    Convert an identifier to a URL
    """
    url = f"/{identifier.replace('_', '/')}"
    return url


class GenericDataPanel(tk.Frame):
    def __init__(self, master, name, identifier, schema):
        super().__init__(master)
        self.text_boxes = {}
        self.name = name
        self.url = f"{definitions.MS_SERVER_HOST}:{definitions.MS_SERVER_PORT}{identifier_to_url(identifier)}"
        self.schema = schema

        self.required_fields = []
        self.missing_fields = []

        # Create frames for layout
        self.left_frame = tk.Frame(self, bg="lightgray", width=200)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Dropdown for Y-axis selection
        self.y_axis_var = tk.StringVar()
        tk.Label(self.left_frame, text="Y-axis:").grid(row=0, column=0,
                                                       columnspan=2, padx=10,
                                                       pady=5, sticky="w")
        self.y_axis_dropdown = ttk.Combobox(self.left_frame,
                                            textvariable=self.y_axis_var,
                                            width=50)  # Increased width
        self.y_axis_dropdown.grid(row=1, column=0, columnspan=2, padx=10,
                                  pady=5, sticky="w")

        # Button to generate the graph
        self.graph_button = tk.Button(self.left_frame, text="Generate Graph",
                                      command=self.generate_graph)
        self.graph_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Right frame for canvas
        self.canvas_frame = tk.Frame(self, bg="white")
        self.canvas_frame.grid(row=0, column=1, padx=10, pady=10,
                               sticky="nsew")

        # Configure resizing behavior
        self.grid_rowconfigure(0, weight=1)  # Allow vertical expansion
        self.grid_columnconfigure(0, weight=1)  # Left frame
        self.grid_columnconfigure(1, weight=3)  # Right frame

    def update_dropdowns(self):
        """
        Update the Y-axis dropdown with
        """
        # flatten the schema from properties
        properties = self.schema.get("properties", {})
        variable_list = flatten_properties(properties)

        # Add the variable list to the Y-axis dropdown
        self.y_axis_dropdown['values'] = variable_list

    def generate_graph(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return

        data = response.json()
        if not data or not isinstance(data, list):
            print("No valid data to display")
            return

        selected_y = self.y_axis_var.get().split(" ")[0]  # strip type info
        filtered_data = [
            item for item in data
            if "timestamp" in item and selected_y in item
        ]

        # Sort by timestamp
        filtered_data.sort(key=lambda item: item["timestamp"])

        # Convert timestamp to datetime and extract y-axis values
        x_axis = [parse(item["timestamp"]) for item in filtered_data]
        y_axis = [item[selected_y] for item in filtered_data]

        if not x_axis or not y_axis:
            print("No matching data found for selected Y-axis.")
            return

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_axis, y_axis)
        ax.set_title(f"{self.name}")
        ax.set_xlabel("Time")
        ax.set_ylabel(selected_y)

        # Adjust layout to prevent clipping
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
