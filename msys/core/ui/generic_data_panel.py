import tkinter as tk
from tkinter import ttk

import requests

from msys.core.generators.open_api.OOP_generator.oop_request_helper import \
    RequestHelper


class GenericDataPanel(tk.Frame):
    def __init__(self, master, panel_name, http_obj):
        super().__init__(master)
        self.text_boxes = None
        self.name = panel_name
        self.http_obj = http_obj
        self.request_helper = RequestHelper(http_obj)
        self.body = None

        label = tk.Label(self, text=f"This is {self.name}")
        label.grid(row=0, column=0, columnspan=2, pady=20)

        self.dropdown_x = None
        self.dropdown_y = None

    def set_params_from_ui(self):
        """
        Set the path params from the UI
        """
        params_spec = self.http_obj.parameters_spec
        self.text_boxes = {}

        for idx, param in enumerate(params_spec):
            param_name = param.get("name")
            param_label = tk.Label(self, text=param_name)
            param_label.grid(row=idx + 1, column=0, padx=10, pady=5,
                             sticky="e")

            enum_values = self.find_enum_values(param.get("schema", {}))
            if enum_values:
                # Create a dropdown for enum values
                selected_option = tk.StringVar()
                dropdown = ttk.Combobox(self, textvariable=selected_option,
                                        values=enum_values)
                dropdown.grid(row=idx + 1, column=1, padx=10, pady=5,
                              sticky="w")
                self.text_boxes[param_name] = dropdown
            else:
                # Create a text box for other parameters
                text_box = tk.Entry(self)
                text_box.grid(row=idx + 1, column=1, padx=10, pady=5,
                              sticky="w")
                self.text_boxes[param_name] = text_box

        self.populate_ui_from_http_obj()

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

    def update_http_obj_from_ui(self):
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

            # Debug print to check the param_value
            print(f"Param Name: {param_name}, Param Value: {param_value}")

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
            self.http_obj.request_args['cookies'] = cookie_params

        # Debug prints to check the parameters set in the request helper
        print(f"Path Params: {path_params}")
        print(f"Query Params: {query_params}")
        print(f"Header Params: {header_params}")
        print(f"Cookie Params: {cookie_params}")

        self.request_helper.make_request()

        if self.request_helper.response.status_code == 200:
            try:
                self.body = self.request_helper.response.json()
            except requests.exceptions.JSONDecodeError:
                self.body = self.request_helper.response.text

        print("URL", self.request_helper.url)
        print("request_args", self.request_helper.request_args)
        print("Body", self.body)
        print("Response", self.request_helper.response)
