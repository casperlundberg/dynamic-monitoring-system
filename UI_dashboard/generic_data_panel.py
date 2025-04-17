import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk

from dateutil.parser import parse

import requests
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from definitions import LEFT_PANEL_WIDTH


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
    def __init__(self, master, identifier):
        super().__init__(master)
        self.text_boxes = {}  # Initialize self.text_boxes as an empty dictionary
        self.name = identifier
        self.body = None

        self.required_fields = []
        self.missing_fields = []

        # Create frames for layout
        self.left_frame = tk.Frame(self, width=LEFT_PANEL_WIDTH, height=1000)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10,
                             sticky="nw")
        self.left_frame.grid_propagate(False)

        # Create a canvas with a vertical scrollbar for the parameters
        # top-left
        self.scroll_canvas = tk.Canvas(self.left_frame, width=LEFT_PANEL_WIDTH,
                                       height=400)
        self.scroll_canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_y = tk.Scrollbar(self.left_frame,
                                        orient="vertical",
                                        command=self.scroll_canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.scroll_canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.inner_frame = tk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=self.inner_frame,
                                         anchor="nw")

        self.inner_frame.bind("<Configure>",
                              lambda e: self.scroll_canvas.configure(
                                  scrollregion=self.scroll_canvas.bbox(
                                      "all")))

        # mid-left with the axis dropdowns and create graph button
        self.axis_controls_frame = tk.Frame(self.left_frame,
                                            width=LEFT_PANEL_WIDTH)
        self.axis_controls_frame.grid(row=1, column=0, columnspan=2,
                                      padx=10, pady=10, sticky="nsew")
        # self.axis_controls_frame.grid_propagate(False)

        # Add widgets to axis_controls_frame
        self.x_axis_var = tk.StringVar()
        self.y_axis_var = tk.StringVar()

        tk.Label(self.axis_controls_frame, text="X-axis:").grid(row=0,
                                                                column=0,
                                                                padx=10,
                                                                pady=5,
                                                                sticky="e")
        self.x_axis_dropdown = ttk.Combobox(self.axis_controls_frame,
                                            textvariable=self.x_axis_var,
                                            width=40)
        self.x_axis_dropdown.grid(row=0, column=1, padx=10, pady=5,
                                  sticky="w")

        tk.Label(self.axis_controls_frame, text="Y-axis:").grid(row=1,
                                                                column=0,
                                                                padx=10,
                                                                pady=5,
                                                                sticky="e")
        self.y_axis_dropdown = ttk.Combobox(self.axis_controls_frame,
                                            textvariable=self.y_axis_var,
                                            width=40)
        self.y_axis_dropdown.grid(row=1, column=1, padx=10, pady=5,
                                  sticky="w")

        self.graph_button = tk.Button(self.axis_controls_frame,
                                      text="Generate Graph",
                                      command=self.generate_graph)
        self.graph_button.grid(row=2, column=0, columnspan=2, pady=10)

        # bottom-left with the response metrics
        self.metrics_frame = tk.Frame(self.left_frame,
                                      width=LEFT_PANEL_WIDTH)
        self.metrics_frame.grid(row=2, column=0, columnspan=1, padx=10,
                                pady=10, sticky="nsew")
        self.metrics_frame.grid_propagate(False)

        # right side: graph
        self.canvas_frame = tk.Frame(self, width=1000, height=400)
        self.canvas_frame.grid(row=0, column=1, padx=10, pady=10,
                               sticky="nsew")
        self.canvas_frame.grid_propagate(False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def get_data(self):
        """
        Get the data from the API
        """

    def extract_fields(self, schema, components, parent_key='body'):
        """
        Recursively extract fields from the schema and components
        """
        fields = []

        if 'properties' in schema:
            print("schema['properties']:\n", json.dumps(schema['properties'],
                                                        indent=4), "\n")

            for key, value in schema['properties'].items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                fields.append(full_key)
                if 'type' in value and value['type'] in components['schemas']:
                    ref_schema = components['schemas'][value['type']]
                    fields.extend(
                        self.extract_fields(ref_schema, components, full_key))
                elif value.get('type') == 'array' and 'items' in value:
                    if 'type' in value['items'] and value['items']['type'] in \
                            components['schemas']:
                        ref_schema = components['schemas'][
                            value['items']['type']]
                        fields.extend(
                            self.extract_fields(ref_schema, components,
                                                full_key))
                    else:
                        fields.extend(
                            self.extract_fields(value['items'], components,
                                                full_key))
                else:
                    fields.extend(
                        self.extract_fields(value, components, full_key))
        return fields

    def update_dropdowns(self):
        """
        Update the X-axis and Y-axis dropdowns with suitable fields from the OpenAPI schema
        """
        responses = self.http_obj.response_spec
        metrics_keys = ["metrics.response_time_ms",
                        "metrics.status_code",
                        "metrics.content_type",
                        "metrics.content_length", "timestamp"]

        if '200' in responses:
            content = responses['200'].get('content', {})

            if 'application/json' in content:
                schema = content['application/json'].get('schema', {})
            # elif 'application/xml' in content:
            #     schema = content['application/xml'].get('schema', {})
            else:
                schema = {}

            # get potential X and Y axis fields from the schema
            components = self.http_obj.components_spec

            if 'properties' not in schema:
                prop_schema = {
                    "properties": find_properties_in_schema(schema,
                                                            components)}
            else:
                prop_schema = schema
            fields = self.extract_fields(prop_schema, components)

            print("fields: ", fields)

            # Add the metrics keys to the fields
            fields.extend(metrics_keys)

            self.x_axis_dropdown['values'] = fields
            self.y_axis_dropdown['values'] = fields

            if self.http_obj.x_axis:
                self.x_axis_var.set(self.http_obj.x_axis)
            if self.http_obj.y_axis:
                self.y_axis_var.set(self.http_obj.y_axis)

        # all 2xx responses
        elif any([str(code).startswith('2') for code in responses.keys()]):
            self.x_axis_dropdown['values'] = metrics_keys
            self.y_axis_dropdown['values'] = metrics_keys
        else:
            print("No 200 response found in response_spec")

    def show_metrics(self):
        """
        Show the metrics for the response
        """
        if not self.body:
            print("No data found in the response")
            return

        pretty_metrics = json.dumps(self.http_obj.metrics, indent=4)
        create_text_with_scrollbar(self.metrics_frame, pretty_metrics,
                                   expand=False)

    def generate_graph(self):
        """
        Generate a graph based on the selected X-axis and Y-axis data
        """
        # # Clear the metrics_frame before adding new widgets
        # for widget in self.metrics_frame.winfo_children():
        #     widget.destroy()

        # Clear the canvas_frame before adding new widgets
        # for widget in self.canvas_frame.winfo_children():
        #     widget.destroy()

        status_code = self.get_data()

        if status_code == 404:
            # pretty print
            pretty_response = json.dumps(self.body, indent=4)
            print("body:\n", pretty_response)
            print("Status code 404: Not found")

        if self.missing_fields:
            # show pop-up with missing fields

            self.missing_fields.clear()
            return

        if self.x_axis_var.get() == '' or self.y_axis_var.get() == '':
            print("Please select both X-axis and Y-axis fields.")
            return

        x_field = self.x_axis_var.get()
        y_field = self.y_axis_var.get()

        x_key_is_in_array = is_key_array_or_nested_deeper({"body": self.body},
                                                          x_field)
        y_key_is_in_array = is_key_array_or_nested_deeper({"body": self.body},
                                                          y_field)

        if not x_key_is_in_array and not y_key_is_in_array:
            # The chosen fields are not in a list
            # and therefore not suitable for plotting
            history_data = self.http_obj.historical_data
            x_data = find_history_data_by_key(history_data, x_field)
            y_data = find_history_data_by_key(history_data, y_field)
            print(f"x_data: {x_data}")
            print(f"y_data: {y_data}")
            if len(x_data) == 0 and len(y_data) == 0:  # if length is 0
                pretty_response = json.dumps(self.body, indent=4)
                create_text_with_scrollbar(self.canvas_frame, pretty_response)

        else:
            x_data = find_value_by_key({"body": self.body}, x_field)
            y_data = find_value_by_key({"body": self.body}, y_field)

        # if x_data is None or y_data is None:
        #     print(f"Could not find data for fields: {x_field}, {y_field}")
        #     print("Re-fetching data...")
        #     self.get_data()
        #
        #     x_data = find_value_by_key(self.body, x_field)
        #     y_data = find_value_by_key(self.body, y_field)

        # check if axes are lists
        ############################################################
        # Should know from the schema if the data is a list or not!!
        ############################################################
        if not isinstance(x_data, list) or not isinstance(y_data, list):
            pretty_response = json.dumps(self.body, indent=4)
            create_text_with_scrollbar(self.canvas_frame, pretty_response)
            print("Error: x_data and y_data must be lists.")

        else:
            # Check if x_data or y_data are strings representing time and convert them
            try:
                x_data = [
                    parse(item) if isinstance(item, str) else item
                    for item in x_data]
            except ValueError:
                pretty_response = json.dumps(self.body, indent=4)
                create_text_with_scrollbar(self.canvas_frame, pretty_response)
                print(f"Error converting x_data to datetime: {x_data}")
                return

            try:
                y_data = [
                    parse(item) if isinstance(item, str) else item
                    for item in y_data]
            except ValueError:
                pretty_response = json.dumps(self.body, indent=4)
                create_text_with_scrollbar(self.canvas_frame, pretty_response)
                print(f"Error converting y_data to datetime: {y_data}")
                return

            if len(x_data) != len(y_data):
                print(
                    f"Error: x_data and y_data must have the same length. x_data length: {len(x_data)}, y_data length: {len(y_data)}")
                return

            # Create a plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_data, y_data, marker='o')
            ax.set_xlabel(x_field)
            ax.set_ylabel(y_field)
            ax.set_title(f"{x_field} vs {y_field}")

            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            self.http_obj.x_axis = x_field
            self.http_obj.y_axis = y_field
