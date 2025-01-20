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
        for FrameClass in (PasswordCheckerApp, gen.GeneratorFrame, ManagerFrame):
            frame = FrameClass(self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Create a bottom navigation bar
        self.create_navigation_bar()

        # Show the initial frame
        self.show_frame(PasswordCheckerApp)

    def create_navigation_bar(self):
        """Create a navigation bar at the bottom of the window."""
        # Add a separator line above the navigation bar
        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=1, column=0, sticky="ew")

        nav_bar = ttk.Frame(self, height=50)
        nav_bar.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Navigation buttons
        tutorial_button = ttk.Button(nav_bar, text="Tutorial", command=lambda: self.show_frame(PasswordCheckerApp), style="Accent.TButton")
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

class PasswordCheckerApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.create_widgets()

    def is_password_secure(self, password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit."
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter."
        if not any(char.islower() for char in password):
            return False, "Password must contain at least one lowercase letter."
        if not any(char in "!@#$%^&*()-_+=" for char in password):
            return False, "Password must contain at least one special character (!@#$%^&*()-_+=)."
        return True, "Password is secure."

    def update_progress_bar(self, value):
        self.security_progress_bar['value'] = value

    def check_password(self):
        password = self.password_entry.get()
        secure, message = self.is_password_secure(password)
        self.result_label.config(text=message, foreground="green" if secure else "red")

        # Update progress bar value based on password security
        if secure:
            self.update_progress_bar(100)
        else:
            length_score = min(len(password) * 3, 30)
            digit_score = 10 if any(char.isdigit() for char in password) else 0
            upper_score = 10 if any(char.isupper() for char in password) else 0
            lower_score = 10 if any(char.islower() for char in password) else 0
            special_score = 30 if any(char in "!@#$%^&*()-_+=" for char in password) else 0
            total_score = length_score + digit_score + upper_score + lower_score + special_score
            self.update_progress_bar(total_score)

    def create_widgets(self):
        password_label = ttk.Label(self, text="Enter a password to check its security:", font=("Arial", 12))
        password_label.grid(row=1, column=0, pady=10, sticky="n")

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=0, pady=10, padx=20, sticky="n")

        check_button = ttk.Button(self, text="Check Password", command=self.check_password)
        check_button.grid(row=3, column=0, pady=10, sticky="n")

        self.result_label = ttk.Label(self, text="", font=("Arial", 12))
        self.result_label.grid(row=4, column=0, pady=10, sticky="n")

        self.security_progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate", maximum=100)
        self.security_progress_bar.grid(row=5, column=0, pady=10, padx=20, sticky="n")

# Run the app
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()