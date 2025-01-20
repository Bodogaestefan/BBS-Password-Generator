import tkinter as tk
from tkinter import ttk, simpledialog
import generator as gen
import tutorial as tut
import manager as man
import repo as repo

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("BBS Password Security App")
        self.geometry("550x500")  # Fixed window size
        self.resizable(False, False)
        self.iconphoto(False, tk.PhotoImage(file="password.png"))
        self.frames = {}
        self.initialize_database()


        # Load the custom dark theme
        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")

        # Configure grid layout for the main window
        self.grid_rowconfigure(0, weight=1)  # Main content area
        self.grid_rowconfigure(1, weight=0)  # Navigation bar
        self.grid_columnconfigure(0, weight=1)

        # Initialize all frames
        for FrameClass in (tut.TutorialFrame, gen.GeneratorFrame, man.ManagerFrame):
            frame = FrameClass(self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Create a bottom navigation bar
        self.create_navigation_bar()

        # Show the initial frame
        self.show_frame(tut.TutorialFrame)

        self.check_vault()

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

        manager_button = ttk.Button(nav_bar, text="Manager", command=lambda: self.show_frame(man.ManagerFrame), style="Accent.TButton")
        manager_button.grid(row=0, column=3, padx=10, pady=10)

        nav_bar.grid(row=2, column=0, sticky="ew")

    def show_frame(self, frame_class):
        """Bring the specified frame to the front."""
        frame = self.frames[frame_class]
        frame.tkraise()

    def initialize_database(self):
        repo.create_tables()

    def check_vault(self):
        if not repo.exists_vault():
            create_vault = simpledialog.askstring("Create Vault", "Enter a name for your new vault:")
            if create_vault is None:  # User pressed cancel
                self.destroy()  # Close the main application
                return
            # Proceed to create the vault if a name was provided
            if create_vault.strip():  # Ensure the name is not empty
                password = man.create_vault(create_vault)
                if password:
                    tk.messagebox.showinfo("Vault Created", f"Vault created successfully. Your new vault password is: {password}. Please keep it safe!")
            else:
                self.destroy()  # Close the app if no valid name was provided



# Run the app
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
