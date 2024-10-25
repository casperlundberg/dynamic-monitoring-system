import tkinter as tk
from tkinter import ttk

from src.core.actions.update import UpdateAction
from src.core.generators.open_api.OOP_generator.oopgenerator import \
    OOPGenerator
from src.core.ui.generic_data_panel import GenericDataPanel


class RootApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.panel_var = None
        self.panel_dropdown = ttk.Combobox()
        self.title("Root Application")
        self.geometry("800x600")

        self.panels = {}
        self.panel_labels = []
        self.current_panel = None

        self.updateAction = UpdateAction()

        # https://raw.githubusercontent.com/swagger-api/swagger-petstore/refs/heads/master/src/main/resources/openapi.yaml
        # Default IDL path
        self.idl_path = "https://raw.githubusercontent.com/open-meteo/open-meteo/refs/heads/main/openapi.yml"

        # Textbox and button to update the interfaces
        self.get_idl_input()

    def call_update_action(self):
        self.updateAction.load_idl_document()
        self.updateAction.dereference_spec()

        generator = OOPGenerator(self.updateAction.idl)
        self.updateAction.update(generator)

        # labels used for each panel header and dropdown
        self.panel_labels = generator.get_client_classnames()

        # update the panels
        self.update_panels()

        # OBS!!! SHOULD NOT BE HERE
        # dropdown to select the panel
        self.update_dropdown()

    def get_idl_input(self):
        # textbox for the user to input the IDL file path
        textbox = tk.Entry(self, width=40)
        textbox.insert(0, self.idl_path)
        textbox.pack(pady=20)

        def update_idl():
            self.idl_path = textbox.get()
            self.updateAction.set_input_path(self.idl_path)
            self.call_update_action()

        button = tk.Button(self, text="Update interfaces", command=update_idl)
        button.pack(pady=20)

    def update_panels(self):
        for panel_name in self.panel_labels:
            # create a panel object for each client class
            panel = GenericDataPanel(self, panel_name)
            self.panels[panel_name] = panel

    def update_dropdown(self):
        self.panel_var = tk.StringVar()
        self.panel_dropdown = ttk.Combobox(self, textvariable=self.panel_var,
                                           values=list(self.panels.keys()))
        self.panel_dropdown.pack(pady=20)
        self.panel_dropdown.bind("<<ComboboxSelected>>",
                                 self.on_panel_selected)

    def on_panel_selected(self, event):
        selected_panel = self.panel_var.get()
        self.show_panel(selected_panel)

    def show_panel(self, panel_name):
        if self.current_panel:
            self.current_panel.pack_forget()
        self.current_panel = self.panels[panel_name]
        self.current_panel.pack(fill="both", expand=True)

        # get the data from the client
        self.current_panel.construct_client()
        self.current_panel.get_data()
        self.current_panel.drop_boxes()
