import tkinter as tk
from tkinter import ttk

from src.core.actions.update import UpdateAction
from src.generated_code.ui import *


class RootApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.panel_var = None
        self.panel_dropdown = None
        self.title("Root Application")
        self.geometry("800x600")

        self.panels = {}
        self.current_panel = None

        self.updateAction = UpdateAction()
        self.idl_path = "C:/Users/Desktop-Lumpa/Downloads/openapi.json"

        # Should get the panel classes from the generator or update action
        # Should also be a set_panel_classes method in this class
        # There is a possibility that the panel classes are not known
        # at the time of instantiation and should be set later by the update action
        self.panel_classes = {}

    def get_idl_input(self):
        # textbox for the user to input the IDL file path
        textbox = tk.Entry(self, width=40)
        textbox.pack(pady=20)

        def on_button_click():
            self.idl_path = textbox.get()

        button = tk.Button(self, text="Submit", command=on_button_click)
        button.pack(pady=20)

        self.updateAction.set_input_path(self.idl_path)

    def update_panel_classes(self):
        panel_classnames_list = self.updateAction.get_panel_classes()
        for panel_classname in panel_classnames_list:
            self.panel_classes[panel_classname] = panel_classname

    def create_panels(self):
        for panel_name, panel_class in self.panel_classes.items():
            self.panels[panel_name] = panel_class(self)

    def create_dropdown(self):
        self.panel_var = tk.StringVar()
        self.panel_dropdown = ttk.Combobox(self, textvariable=self.panel_var,
                                           values=list(
                                               self.panel_classes.keys()))
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
