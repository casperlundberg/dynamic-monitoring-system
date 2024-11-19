import tkinter as tk
from tkinter import ttk

from msys.core.generators.open_api.models.http_model import HTTPModel
from msys.core.ui.generic_data_panel import GenericDataPanel
from shared_data import shared_queue, update_event
from utils import serialize_save_file, deserialize_save_file


class RootApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.panel_var = tk.StringVar()
        self.title("Root Application")
        self.geometry("1920x1080+0+0")
        self.state("zoomed")

        self.panels = {}
        self.panel_templates = {}
        self.save_file_name = "panel_data_obj_list"
        self.current_panel = None

        save_button = tk.Button(self, text="Save session",
                                command=self.save_data)
        save_button.grid(row=0, column=2, padx=10, pady=10)

        self.crete_new_panel = tk.Button(self, text="Create panel",
                                         command=self.create_panel_from_template)
        self.crete_new_panel.grid(row=0, column=1, padx=10, pady=10)

        self.panel_dropdown = ttk.Combobox(self, textvariable=self.panel_var)
        self.panel_dropdown.grid(row=0, column=0, columnspan=1, padx=10,
                                 pady=10)
        self.panel_dropdown.bind("<<ComboboxSelected>>",
                                 self.on_panel_selected)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Load previous settings on start
        self.load_data()

        # Start the loop that waits for updates from the generator
        self.check_for_updates()

    def check_for_updates(self):
        if update_event.is_set():
            generator = shared_queue.get()  # Get the generator object from the queue
            self.update_panels(generator)
            update_event.clear()  # Clear the event

        self.after(100,
                   self.check_for_updates)  # Check for updates every 100ms

    def update_panels(self, generator):
        # self.panel_templates.update(generator.http_data_objs.copy())
        # Update the UI with the new generator object
        for k, v in generator.http_data_objs.items():
            self.panels[k] = GenericDataPanel(self, k, v)
            # self.panel_templates[k] = v
            self.panel_templates[k] = HTTPModel(
                PATH=v.PATH,
                SERVER=v.SERVER,
                path_params=v.path_params.copy(),
                request_args={},
                url=v.url,
                response_body={},
                metrics={},
                x_axis="",
                y_axis="",
                parameters_spec=v.parameters_spec.copy() if v.parameters_spec else {},
                response_spec=v.response_spec.copy() if v.response_spec else {},
                components_spec=v.components_spec.copy() if v.components_spec else {},
                http_method=v.http_method,
                response_type="",
                historical_data=[]
            )
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
        self.current_panel.grid(row=1, column=0, columnspan=3, padx=10,
                                pady=10, sticky="nsew")

        # get params before getting data
        self.current_panel.set_params_from_ui()

        # Show the "Get Data" button

    def create_panel_from_template(self):
        # create pop-up window with form to fill in
        top = tk.Toplevel(self)
        top.geometry("550x450")
        top.title("Create new panel")
        label = tk.Label(top, text="Enter the name of the new panel")
        label.pack()
        name_entry = tk.Entry(top)
        name_entry.pack()
        drop_down_label = tk.Label(top, text="Select the target endpoint")
        drop_down_label.pack()
        drop_down = ttk.Combobox(top)
        drop_down.pack()
        drop_down['values'] = list(self.panel_templates.keys())

        button = tk.Button(top, text="Create",
                           command=lambda: self.template_to_panel(
                               name_entry.get(),
                               self.panel_templates[drop_down.get()]))
        button.pack()

    def template_to_panel(self, name, http_obj):
        # Add a new panel to the list
        new_panel_data = HTTPModel(
            PATH=http_obj.PATH,
            SERVER=http_obj.SERVER,
            path_params=http_obj.path_params.copy(),
            request_args=http_obj.request_args.copy(),
            url=http_obj.url,
            response_body={},
            metrics={},
            x_axis="",
            y_axis="",
            parameters_spec=http_obj.parameters_spec.copy(),
            response_spec=http_obj.response_spec.copy(),
            components_spec=http_obj.components_spec.copy(),
            http_method=http_obj.http_method,
            response_type=http_obj.response_type,
            historical_data=[]
        )

        self.panels[name] = GenericDataPanel(self, name, new_panel_data)
        self.update_dropdown()

    def save_data(self):
        # Update the http_obj with the current values from the UI elements
        for panel in self.panels.values():
            panel.update_http_obj_from_ui()

        # Update http_data_objs with the new http_objs from each panel
        http_data_objs = {k: panel.http_obj for k, panel in
                          self.panels.items()}

        # Save http_data_objs to the file
        serialize_save_file(http_data_objs, self.save_file_name)
        print(f"Data saved to {self.save_file_name}: {http_data_objs}")

        # Save unique_endpoints to the file
        serialize_save_file(self.panel_templates, "unique_endpoints")

    def load_data(self):
        http_data_objs = deserialize_save_file(self.save_file_name)
        if http_data_objs is None:
            return
        for k, v in http_data_objs.items():
            self.panels[k] = GenericDataPanel(self, k, v)
            self.panels[
                k].populate_ui_from_http_obj()  # Populate UI with loaded data
            self.panels[
                k].update_dropdowns()  # Update dropdowns with loaded data
        self.update_dropdown()
        print(f"Data loaded from {self.save_file_name}")

        # Load unique_endpoints from the file
        self.panel_templates = deserialize_save_file("unique_endpoints")
