import tkinter as tk
from tkinter import ttk

class TutorialFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Configure grid to center content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Add content
        label = ttk.Label(self, text="Welcome to the Security Tutorial", font=("Arial", 18))
        label.grid(row=0, column=0, pady=20, sticky="n")

        text = ttk.Label(self, text=(
            "Security is essential in the digital world. Using strong and unique passwords "
            "for your accounts is critical to protecting your data and privacy.\n\n"
            "This app provides tools for generating and managing secure passwords."
        ), font=("Arial", 12), justify="center", wraplength=500)
        text.grid(row=1, column=0, pady=10, padx=20, sticky="n")