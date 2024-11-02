from datetime import datetime
import tkinter as tk
from tkinter import ttk

import requests
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from msys.core.generators.open_api.OOP_generator.oop_request_helper import \
    RequestHelper


class GenericDataPanel(tk.Frame):
    def __init__(self, master, panel_name, http_obj):
        super().__init__(master)
        self.text_boxes = {}  # Initialize self.text_boxes as an empty dictionary
        self.name = panel_name
        self.http_obj = http_obj
        self.request_helper = RequestHelper(http_obj)
        self.body = None

        # Create frames for layout
        self.params_frame = tk.Frame(self)
        self.params_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.canvas_frame = tk.Frame(self, width=1000, height=600)
        self.canvas_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10,
                               sticky="nsew")
        self.canvas_frame.grid_propagate(False)

        self.canvas = None

        # Create a canvas with scrollbars for the parameters
        self.scroll_canvas = tk.Canvas(self.params_frame, width=400,
                                       height=400)
        self.scroll_canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_y = tk.Scrollbar(self.params_frame, orient="vertical",
                                        command=self.scroll_canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.scrollbar_x = tk.Scrollbar(self.params_frame, orient="horizontal",
                                        command=self.scroll_canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.scroll_canvas.configure(yscrollcommand=self.scrollbar_y.set,
                                     xscrollcommand=self.scrollbar_x.set)

        self.inner_frame = tk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=self.inner_frame,
                                         anchor="nw")

        self.inner_frame.bind("<Configure>",
                              lambda e: self.scroll_canvas.configure(
                                  scrollregion=self.scroll_canvas.bbox("all")))

        # Create a frame for the axis dropdowns and graph button
        self.axis_controls_frame = tk.Frame(self.params_frame)
        self.axis_controls_frame.grid(row=2, column=0, columnspan=2, padx=10,
                                      pady=10, sticky="nsew")

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
        self.x_axis_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self.axis_controls_frame, text="Y-axis:").grid(row=1,
                                                                column=0,
                                                                padx=10,
                                                                pady=5,
                                                                sticky="e")
        self.y_axis_dropdown = ttk.Combobox(self.axis_controls_frame,
                                            textvariable=self.y_axis_var,
                                            width=40)
        self.y_axis_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.graph_button = tk.Button(self.axis_controls_frame,
                                      text="Generate Graph",
                                      command=self.generate_graph)
        self.graph_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def set_params_from_ui(self):
        """
        Set the path params from the UI
        """
        params_spec = self.http_obj.parameters_spec
        self.text_boxes = {}  # Ensure self.text_boxes is initialized

        for idx, param in enumerate(params_spec):
            param_name = param.get("name")
            param_label = tk.Label(self.inner_frame, text=param_name)
            param_label.grid(row=idx, column=0, padx=10, pady=5, sticky="e")

            enum_values = self.find_enum_values(param.get("schema", {}))
            if enum_values:
                # Create a dropdown for enum values
                selected_option = tk.StringVar()
                dropdown = ttk.Combobox(self.inner_frame,
                                        textvariable=selected_option,
                                        values=enum_values,
                                        width=40)
                dropdown.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
                self.text_boxes[param_name] = dropdown
                dropdown.bind("<<ComboboxSelected>>",
                              self.update_http_obj_from_ui)
            else:
                # Create a text box for other parameters
                text_box = tk.Entry(self.inner_frame, width=40)
                text_box.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
                self.text_boxes[param_name] = text_box
                text_box.bind("<KeyRelease>", self.update_http_obj_from_ui)

        self.populate_ui_from_http_obj()
        self.update_dropdowns()  # Update dropdowns immediately

    def populate_ui_from_http_obj(self):
        """
        Populate the UI elements with values from the http_obj
        """
        for param_name, widget in self.text_boxes.items():
            if param_name in self.http_obj.path_params:
                value = self.http_obj.path_params[param_name]
            elif param_name in self.http_obj.request_args.get('params', {}):
                value = self.http_obj.request_args['params'][param_name]
            elif param_name in self.http_obj.request_args.get('headers', {}):
                value = self.http_obj.request_args['headers'][param_name]
            elif param_name in self.http_obj.request_args.get('cookies', {}):
                value = self.http_obj.request_args['cookies'][param_name]
            else:
                value = None

            if value is not None:
                if isinstance(widget, ttk.Combobox):
                    widget.set(value)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, value)

    def update_http_obj_from_ui(self, event=None):
        """
        Update the http_obj with values from the UI elements
        """
        for param_name, widget in self.text_boxes.items():
            param_value = widget.get()
            if param_name in self.http_obj.path_params:
                self.http_obj.path_params[param_name] = param_value
            elif param_name in self.http_obj.request_args.get('params', {}):
                self.http_obj.request_args['params'][param_name] = param_value
            elif param_name in self.http_obj.request_args.get('headers', {}):
                self.http_obj.request_args['headers'][param_name] = param_value
            elif param_name in self.http_obj.request_args.get('cookies', {}):
                self.http_obj.request_args['cookies'][param_name] = param_value

    def find_enum_values(self, schema):
        """
        Recursively find enum values in the schema
        """
        if "enum" in schema:
            return schema["enum"]
        elif "items" in schema:
            return self.find_enum_values(schema["items"])
        elif "properties" in schema:
            for prop in schema["properties"].values():
                enum_values = self.find_enum_values(prop)
                if enum_values:
                    return enum_values
        return None

    def get_data(self):
        """
        Get the data from the client
        """
        params_spec = self.http_obj.parameters_spec
        query_params = {}
        path_params = {}
        header_params = {}
        cookie_params = {}

        for param in params_spec:
            param_name = param.get("name")
            param_value = self.text_boxes[param_name].get()

            if param_value:  # Only add the parameter if it has a value
                if param.get("in") == "path":
                    path_params[param_name] = param_value
                elif param.get("in") == "query":
                    if self.find_enum_values(param.get("schema", {})):
                        enums = self.find_enum_values(param.get("schema", {}))
                        if param_value in enums:
                            query_params[param_name] = param_value
                    else:
                        query_params[param_name] = param_value
                elif param.get("in") == "header":
                    header_params[param_name] = param_value
                elif param.get("in") == "cookie":
                    cookie_params[param_name] = param_value

        # Set the parameters in the request helper
        if path_params:
            self.request_helper.set_path_params(path_params)
            self.http_obj.path_params = path_params
        if query_params:
            self.request_helper.set_query_params(query_params)
            self.http_obj.request_args['params'] = query_params
        if header_params:
            self.request_helper.set_header_params(header_params)
            self.http_obj.request_args['headers'] = header_params
        if cookie_params:
            self.request_helper.set_cookie_params(cookie_params)

        self.request_helper.make_request()

        if self.request_helper.response.status_code == 200:
            try:
                self.body = self.request_helper.response.json()
            except requests.exceptions.JSONDecodeError:
                self.body = self.request_helper.response.text

    def extract_fields(self, schema, components, parent_key=''):
        """
        Recursively extract fields from the schema and components
        """
        fields = []
        if 'properties' in schema:
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

        if '200' in responses:
            content = responses['200'].get('content', {})

            if 'application/json' in content:
                schema = content['application/json'].get('schema', {})
            elif 'application/xml' in content:
                schema = content['application/xml'].get('schema', {})
            else:
                schema = {}

            components = self.http_obj.components_spec
            fields = self.extract_fields(schema, components)
            self.x_axis_dropdown['values'] = fields
            self.y_axis_dropdown['values'] = fields
        else:
            print("No 200 response found in response_spec")

    def generate_graph(self):
        """
        Generate a graph based on the selected X-axis and Y-axis data
        """
        if not self.body:
            self.get_data()

        x_field = self.x_axis_var.get()
        y_field = self.y_axis_var.get()

        if not x_field or not y_field:
            print("Please select both X-axis and Y-axis fields.")
            return

        x_data = find_value_by_key(self.body, x_field)
        y_data = find_value_by_key(self.body, y_field)

        if x_data is None or y_data is None:
            print(f"Could not find data for fields: {x_field}, {y_field}")
            print("Re-fetching data...")
            self.get_data()

            x_data = find_value_by_key(self.body, x_field)
            y_data = find_value_by_key(self.body, y_field)

        # Check if x_data or y_data are strings representing time and convert them
        try:
            x_data = [
                datetime.fromisoformat(item) if isinstance(item, str) else item
                for item in x_data]
        except ValueError:
            print(f"Error converting x_data to datetime: {x_data}")
            return

        try:
            y_data = [
                datetime.fromisoformat(item) if isinstance(item, str) else item
                for item in y_data]
        except ValueError:
            print(f"Error converting y_data to datetime: {y_data}")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_data, y_data, marker='o')
        ax.set_xlabel(x_field)
        ax.set_ylabel(y_field)
        ax.set_title(f"{x_field} vs {y_field}")

        # Embed the plot in the tkinter frame
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def find_value_by_key(data, key):
    """
    Recursively search through the response body to find the value for the given key
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
