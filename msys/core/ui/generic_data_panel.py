import tkinter as tk

from tkinter import ttk

from jsonref import requests

from msys.core.generators.open_api.OOP_generator.oop_request_helper import \
    RequestHelper
import importlib
import pkgutil
import msys.generated_code.clients


def import_modules():
    # Iterate through all modules in the msys.generated_code.clients package
    for _, module_name, _ in pkgutil.iter_modules(
            msys.generated_code.clients.__path__):
        # Import the module
        module = importlib.import_module(
            f"msys.generated_code.clients.{module_name}")
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

        self.dropdown_x = None
        self.dropdown_y = None

    def construct_client(self):
        """
        Construct the client object from the generated code
        """
        import_modules()

        locals_dict = {}
        code = (
            f"dataclass = {self.name}()"
        )

        exec(code, globals(), locals_dict)

        dataclass = locals_dict["dataclass"]
        self.request_helper = RequestHelper(dataclass)

    def get_data(self):
        """
        Get the data from the client
        """
        self.request_helper.make_request()

        if self.request_helper.response.status_code == 200:
            try:
                self.body = self.request_helper.response.json()
            except requests.exceptions.JSONDecodeError:
                self.body = self.request_helper.response.text

    def drop_boxes(self):
        """
        Create the dropdowns for the panel
        """
        print("body: ", self.body)
        options_x_axis = list(nested_dict_keys_to_list(self.body))
        options_y_axis = list(nested_dict_keys_to_list(self.body))

        if self.dropdown_x and self.dropdown_x.winfo_exists():
            self.dropdown_x['values'] = options_x_axis
        else:
            selected_option_x = tk.StringVar()
            self.dropdown_x = ttk.Combobox(self,
                                           textvariable=selected_option_x,
                                           values=options_x_axis)
            self.dropdown_x.pack(pady=20)

        if self.dropdown_y and self.dropdown_y.winfo_exists():
            self.dropdown_y['values'] = options_y_axis
        else:
            selected_option_y = tk.StringVar()
            self.dropdown_y = ttk.Combobox(self,
                                           textvariable=selected_option_y,
                                           values=options_y_axis)
            self.dropdown_y.pack(pady=20)

        x = nested_dict_get_value(self.body, self.dropdown_x.get())
        y = nested_dict_get_value(self.body, self.dropdown_y.get())

        return x, y
