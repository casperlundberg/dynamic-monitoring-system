import tkinter as tk
from tkinter import ttk

from msys.core.ui.generic_data_panel import GenericDataPanel
from shared_data import shared_queue, update_event
from utils import save_client_file_obj, load_client_file_obj


class RootApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.panel_var = tk.StringVar()
        self.title("Root Application")
        self.geometry("960x800")

        self.panels = {}
        self.save_file_name = "panel_obj_list"
        self.current_panel = None

        save_button = tk.Button(self, text="Save session",
                                command=self.save_data)
        save_button.grid(row=0, column=0, padx=10, pady=10)

        load_button = tk.Button(self, text="Load old session",
                                command=self.load_data)
        load_button.grid(row=0, column=1, padx=10, pady=10)

        self.get_data_button = tk.Button(self, text="Get Data",
                                         command=self.get_data)
        self.get_data_button.grid(row=0, column=2, padx=10, pady=10)
        self.get_data_button.grid_remove()  # Initially hide the button

        self.panel_dropdown = ttk.Combobox(self, textvariable=self.panel_var)
        self.panel_dropdown.grid(row=1, column=0, columnspan=3, padx=10,
                                 pady=10)
        self.panel_dropdown.bind("<<ComboboxSelected>>",
                                 self.on_panel_selected)

        self.http_data_objs = {}

        self.check_for_updates()

    def check_for_updates(self):
        if update_event.is_set():
            generator = shared_queue.get()  # Get the generator object from the queue
            self.update_panels(generator)
            update_event.clear()  # Clear the event

        self.after(100,
                   self.check_for_updates)  # Check for updates every 100ms

    def update_panels(self, generator):
        # Update the UI with the new generator object
        self.http_data_objs = generator.http_data_objs
        for k, v in generator.http_data_objs.items():
            self.panels[k] = GenericDataPanel(self, k, v)
        self.update_dropdown()

    def update_dropdown(self):
        self.panel_dropdown['values'] = list(self.panels.keys())

    def on_panel_selected(self, event):
        selected_panel = self.panel_var.get()
        self.show_panel(selected_panel)

    def show_panel(self, panel_name):
        if self.current_panel:
            self.current_panel.grid_remove()
        self.current_panel = self.panels[panel_name]
        self.current_panel.grid(row=2, column=0, columnspan=3, padx=10,
                                pady=10, sticky="nsew")

        # get params before getting data
        self.current_panel.set_params_from_ui()

        # Show the "Get Data" button
        self.get_data_button.grid()

    def get_data(self):
        # get data from the client
        self.current_panel.get_data()

        # update the panel object in the panels dict
        self.http_data_objs[
            self.current_panel.name] = self.current_panel.http_obj

    def save_data(self):
        # Update the http_obj with the current values from the UI elements
        for panel in self.panels.values():
            panel.update_http_obj_from_ui()

        # save http_data_objs inside the panels
        save_client_file_obj(self.http_data_objs, self.save_file_name)

    def load_data(self):
        self.http_data_objs = load_client_file_obj(self.save_file_name)
        for k, v in self.http_data_objs.items():
            self.panels[k] = GenericDataPanel(self, k, v)
        self.update_dropdown()
