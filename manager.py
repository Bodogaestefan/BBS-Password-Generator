import repo
import tkinter as tk
from tkinter import ttk, simpledialog

class ManagerFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master_pwd = None
        self.vault_name = None

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Add content
        label = ttk.Label(self, text="Password Manager", font=("Arial", 18))
        label.grid(row=0, column=0, pady=20, sticky="n")

        text = ttk.Label(self, text="Store and manage your passwords securely here.",
                         font=("Arial", 12), wraplength=500, justify="center")
        text.grid(row=1, column=0, pady=10, sticky="n")

        # Create a Treeview widget to display passwords
        self.password_table = ttk.Treeview(self, columns=("what_for", "uname", "em_addr", "password"), show="headings")
        self.password_table.heading("what_for", text="What For")
        self.password_table.heading("uname", text="Username")
        self.password_table.heading("em_addr", text="Email Address")
        self.password_table.heading("password", text="Password")

        # Set column widths
        self.password_table.column("what_for", width=100)
        self.password_table.column("uname", width=100)
        self.password_table.column("em_addr", width=150)
        self.password_table.column("password", width=100)

        self.password_table.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

        # Add a scrollbar to the table
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.password_table.yview)
        self.password_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky="ns")

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.refresh_table()
        self.authenticate()

    def authenticate(self):
        check_password = simpledialog.askstring("Authenticate", "Enter your vault password:", parent=self)
        if check_password is None:
            return
        if check_password.strip():
            self.vault_name = repo.get_vault_name()
            key_salt = repo.authenticate(self.vault_name, check_password)
            if key_salt:
                tk.messagebox.showinfo("Authentication Successful",
                                       "You have successfully authenticated to your vault.")
                self.master_password = check_password.strip()
                self.load_passwords()
            else:
                tk.messagebox.showerror("Authentication Failed", "Please check your credentials and try again.")
                self.master.destroy()

    def load_passwords(self):
        passwords = repo.retrieve_all_passwords(self.master_password, self.vault_name)  # Replace with actual master password and vault name
        for pwd in passwords:
            self.password_table.insert("", "end", values=pwd)

    def refresh_table(self):
        # Clear existing entries in the table
        for item in self.password_table.get_children():
            self.password_table.delete(item)