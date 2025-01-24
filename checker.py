import tkinter as tk
from tkinter import ttk

class CheckerFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5), weight=1)
        self.create_widgets()

    def has_consecutive_numbers(self, password):
        for i in range(len(password) - 1):
            if password[i].isdigit() and password[i + 1].isdigit():
                return True
        return False

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
        if self.has_consecutive_numbers(password): return False, "Password has consecutive digits"
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
            length_score = min(len(password) * 2, 20)
            digit_score = 10 if any(char.isdigit() for char in password) else 0
            upper_score = 10 if any(char.isupper() for char in password) else 0
            lower_score = 10 if any(char.islower() for char in password) else 0
            special_score = 20 if any(char in "!@#$%^&*()-_+=" for char in password) else 0
            consec_score = -10 if self.has_consecutive_numbers(password) else 0
            total_score = length_score + digit_score + upper_score + lower_score + special_score + consec_score
            self.update_progress_bar(total_score)

    def create_widgets(self):
        title_label = ttk.Label(self, text="Password Checker", font=("Arial", 18))
        title_label.grid(row=0, column=0, pady=20, sticky="n")
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
