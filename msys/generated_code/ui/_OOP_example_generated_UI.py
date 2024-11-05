import tkinter as tk
from tkinter import ttk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from msys.core.generators.open_api.OOP_generator.oop_request_helper import \
    RequestHelper
from msys.core.generators.open_api.models.http_model import ClassName


# Should this file be some sort of panel/graph object??
# That the UI can add to the main window.
# That would mean that this object would call the
# RequestHelper class with methods like set_path_params also in this object.
# That seems like unnecessary code complexity, but it would make the UI code cleaner.

# Maybe the UI should just call the RequestHelper class directly but that
# not make sense as parts of the core UI code would be generated which defy
# the structure of the project.


class ClassNameUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.classname = ClassName()
        self.request_helper = RequestHelper(self.classname)

        label = tk.Label(self, text=f"This is {self.__class__.__name__}")
        label.pack(pady=20)

        # button = tk.Button(self, text="get data", command=self.get_data)

        # HTTP RESPONSE DATA
        body = get_data(self.request_helper)

        # Dropdowns for x values
        options_x_axis = list(nested_dict_keys_to_list(body))
        selected_option_x = tk.StringVar()
        dropdown_x = ttk.Combobox(self, textvariable=selected_option_x,
                                  values=options_x_axis)
        dropdown_x.pack(pady=20)

        # Dropdowns for y values
        options_y_axis = list(nested_dict_keys_to_list(body))
        selected_option_y = tk.StringVar()
        dropdown_y = ttk.Combobox(self, textvariable=selected_option_y,
                                  values=options_y_axis)
        dropdown_y.pack(pady=20)

        x = nested_dict_get_value(body, dropdown_x.current())
        y = nested_dict_get_value(body, dropdown_y.current())

        fig, ax = plt.subplots()
        ax.plot([0, 1, 2, 3], [0, 1, 4, 9])
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

# class_name = PetPetId()
# request_helper = RequestHelper(class_name)
# request_helper.set_path_params({"petId": 10})
# request_helper.make_request()
#
# print(class_name.url)
# try:
#     print(class_name.response.json())
# except requests.exceptions.JSONDecodeError:
#     print(class_name.response.text)
# print(class_name.metrics)
