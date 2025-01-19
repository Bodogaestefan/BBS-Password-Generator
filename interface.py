import tkinter as tk
from tkinter import ttk
import generator as gen
import tutorial as tut

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("BBS Password Security App")
        self.geometry("550x500")  # Fixed window size
        self.resizable(False, False)
        self.iconphoto(False, tk.PhotoImage(file="password.png"))
        self.frames = {}

        # Load the custom dark theme
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")

        # Configure grid layout for the main window
        self.grid_rowconfigure(0, weight=1)  # Main content area
        self.grid_rowconfigure(1, weight=0)  # Navigation bar
        self.grid_columnconfigure(0, weight=1)

        # Initialize all frames
        for FrameClass in (tut.TutorialFrame, gen.GeneratorFrame, ManagerFrame):
            frame = FrameClass(self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Create a bottom navigation bar
        self.create_navigation_bar()

        # Show the initial frame
        self.show_frame(tut.TutorialFrame)

    def create_navigation_bar(self):
        """Create a navigation bar at the bottom of the window."""
        # Add a separator line above the navigation bar
        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=1, column=0, sticky="ew")

        nav_bar = ttk.Frame(self, height=50)
        nav_bar.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Navigation buttons
        tutorial_button = ttk.Button(nav_bar, text="Tutorial", command=lambda: self.show_frame(tut.TutorialFrame), style="Accent.TButton")
        tutorial_button.grid(row=0, column=1, padx=10, pady=10)

        generator_button = ttk.Button(nav_bar, text="Generator", command=lambda: self.show_frame(gen.GeneratorFrame), style="Accent.TButton")
        generator_button.grid(row=0, column=2, padx=10, pady=10)

        manager_button = ttk.Button(nav_bar, text="Manager", command=lambda: self.show_frame(ManagerFrame), style="Accent.TButton")
        manager_button.grid(row=0, column=3, padx=10, pady=10)

        nav_bar.grid(row=2, column=0, sticky="ew")

    def show_frame(self, frame_class):
        """Bring the specified frame to the front."""
        frame = self.frames[frame_class]
        frame.tkraise()

class ManagerFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Add content
        label = tk.Label(self, text="Password Manager", font=("Arial", 18))
        label.grid(row=0, column=0, pady=20, sticky="n")

        text = tk.Label(self, text="Store and manage your passwords securely here.",
                        font=("Arial", 12), wraplength=500, justify="center")
        text.grid(row=1, column=0, pady=10, sticky="n")

        # Example of adding saved passwords (in memory for simplicity)
        self.password_list = tk.Listbox(self, font=("Arial", 12), width=40, height=8)
        self.password_list.grid(row=2, column=0, pady=10, padx=20, sticky="n")

        add_button = tk.Button(self, text="Add Example Password", font=("Arial", 12),
                               command=self.add_example_password)
        add_button.grid(row=3, column=0, pady=10, sticky="n")

    def add_example_password(self):
        self.password_list.insert("end", "example@password123")


# Run the app
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
