import tkinter as tk
from tkinter import ttk

from UI_dashboard.generic_data_panel import GenericDataPanel
from UI_dashboard.queue import update_event, shared_queue
from packages.identifier.identfier import create_identifier


class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.panel_var = tk.StringVar()
        self.title("Monitoring Dashboard")
        self.geometry("1280x480+0+0")
        # self.state("zoomed")

        self.panels = {}
        self.panel_templates = {}
        self.save_file_name = "panel_data_obj_list"
        self.current_panel = None

        # save_button = tk.Button(self, text="Save session",
        #                         command=self.save_data)
        # save_button.grid(row=0, column=2, padx=10, pady=10)

        # self.crete_new_panel = tk.Button(self, text="Create panel",
        #                                  command=self.create_panel_from_template)
        # self.crete_new_panel.grid(row=0, column=1, padx=10, pady=10)

        self.panel_dropdown = ttk.Combobox(self, textvariable=self.panel_var,
                                           width=50)
        self.panel_dropdown.grid(row=0, column=0, columnspan=1, padx=10,
                                 pady=10)
        self.panel_dropdown.bind("<<ComboboxSelected>>",
                                 self.on_panel_selected)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Load previous settings on start
        # self.load_data()

        # Start the loop that waits for updates from the generator
        self.check_for_updates()

    def check_for_updates(self):
        if update_event.is_set():
            spec = shared_queue.get()  # Get the generator object from the queue
            self.update_panels(spec)
            update_event.clear()  # Clear the event

            # print(f"[UI] Spec updated: {spec}")

        self.after(100,
                   self.check_for_updates)  # Check for updates every 100ms

    def update_panels(self, spec):
        # loop through the spec and create a panel for each endpoint
        # pass the identifier to the panel
        for path, path_obj in spec.get("paths").items():
            for method in path_obj.keys():
                ident = create_identifier(spec, path, method)
                if ident not in self.panels:
                    # get schema for the current path
                    method_prefix = ident.split("_", 1)[0].lower()

                    print(
                        f"[UI] Found new endpoint: {ident}, method: {method_prefix}")

                    # Get schema using the actual method from path_obj
                    operation_obj = path_obj.get(method_prefix)
                    if not operation_obj:
                        print(
                            f"[UI] Skipping {ident}, method '{method_prefix}' not found in path")
                        continue

                    request_body = operation_obj.get("requestBody", {})
                    schema = request_body.get("content", {}).get(
                        "application/json", {}).get("schema")

                    if not schema:
                        print(f"[UI] No schema found for {ident}")
                        continue

                    self.panels[ident] = GenericDataPanel(self, ident, ident,
                                                          schema)
                    self.update_dropdown()

                    self.panel_templates[ident] = ident
                    self.panels[ident].update_dropdowns()

    def update_dropdown(self):
        self.panel_dropdown['values'] = list(self.panels.keys())
        # repaint the dropdown
        self.panel_dropdown.update()

    def on_panel_selected(self, event):
        selected_panel = self.panel_var.get()
        self.show_panel(selected_panel)

    def show_panel(self, panel_name):
        if self.current_panel:
            self.current_panel.grid_remove()
        self.current_panel = self.panels[panel_name]
        self.current_panel.grid(row=1, column=0, columnspan=3, padx=10,
                                pady=10, sticky="nsew")

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
        name = name_entry.get()
        identifier = drop_down.get()
        schema = self.panels[identifier].schema.copy()

        button = tk.Button(top, text="Create",
                           command=lambda: self.template_to_panel(
                               name, identifier, schema))
        button.pack()

    def template_to_panel(self, name, identifier, schema):
        # Add a new panel to the list
        # name is the name of the panel in the ui, identifier is used to get data from the correct endpoint

        self.panels[name] = GenericDataPanel(self, name, identifier, schema)
        self.update_dropdown()
