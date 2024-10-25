import tkinter as tk

from tkinter import ttk

from src.core.generators.open_api.OOP_generator.oop_request_helper import \
    RequestHelper
import importlib
import pkgutil
import src.generated_code.clients

# Iterate through all modules in the src.generated_code.clients package
for _, module_name, _ in pkgutil.iter_modules(
        src.generated_code.clients.__path__):
    # Import the module
    module = importlib.import_module(
        f"src.generated_code.clients.{module_name}")
    # Import all classes from the module
    globals().update({name: cls for name, cls in module.__dict__.items() if
                      isinstance(cls, type)})


def nested_dict_keys_to_list(d):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from nested_dict_keys_to_list(v)
        else:
            yield k


def nested_dict_get_value(d, key):
    for k, v in d.items():
        if k == key:
            return v
        if isinstance(v, dict):
            return nested_dict_get_value(v, key)


class GenericDataPanel(tk.Frame):
    def __init__(self, master=None, panel_name=None):
        super().__init__(master)

        self.name = panel_name
        self.request_helper = None
        self.body = None

        label = tk.Label(self, text=f"This is {self.name}")
        label.pack(pady=20)

        # button = tk.Button(self, text="get data", command=self.get_data)

    def construct_client(self):
        """
        Construct the client object from the generated code
        """
        locals_dict = {}
        code = (
            # f"from src.generated_code.clients import *\n"
            f"client_class = {self.name}()"
        )

        print(code)
        exec(code, globals(), locals_dict)

        client = locals_dict[f"client_class"]
        self.request_helper = RequestHelper(client)

    def get_data(self):
        """
        Get the data from the client
        """
        self.request_helper.make_request()

        if self.request_helper.interface.response.status_code == 200:
            self.body = self.request_helper.interface.response.json()

    def drop_boxes(self):
        """
        Create the dropdowns for the panel
        """

        options_x_axis = list(nested_dict_keys_to_list(self.body))
        selected_option_x = tk.StringVar()
        dropdown_x = ttk.Combobox(self, textvariable=selected_option_x,
                                  values=options_x_axis)
        dropdown_x.pack(pady=20)

        options_y_axis = list(nested_dict_keys_to_list(self.body))
        selected_option_y = tk.StringVar()
        dropdown_y = ttk.Combobox(self, textvariable=selected_option_y,
                                  values=options_y_axis)
        dropdown_y.pack(pady=20)

        x = nested_dict_get_value(self.body, dropdown_x.current())
        y = nested_dict_get_value(self.body, dropdown_y.current())

        return x, y
