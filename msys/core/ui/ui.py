import tkinter as tk
from tkinter import ttk

from msys.core.ui.generic_data_panel import GenericDataPanel
from shared_data import shared_queue, update_event


class RootApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.panel_var = tk.StringVar()
        self.panel_dropdown = ttk.Combobox(self, textvariable=self.panel_var)
        self.title("Root Application")
        self.geometry("800x600")

        self.panels = {}
        self.current_panel = None

        self.panel_dropdown.pack(pady=20)
        self.panel_dropdown.bind("<<ComboboxSelected>>",
                                 self.on_panel_selected)

        self.generator = None

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
        for k, v in generator.http_data_objs.items():
            self.panels[k] = GenericDataPanel(self, k, v)
        self.generator = generator
        self.update_dropdown()

    def update_dropdown(self):
        self.panel_dropdown['values'] = list(self.panels.keys())

    def on_panel_selected(self, event):
        selected_panel = self.panel_var.get()
        self.show_panel(selected_panel)

    def show_panel(self, panel_name):
        if self.current_panel:
            self.current_panel.pack_forget()
        self.current_panel = self.panels[panel_name]
        self.current_panel.pack(fill="both", expand=True)

        # get params before getting data

        self.current_panel.get_data()
        self.current_panel.drop_boxes()
