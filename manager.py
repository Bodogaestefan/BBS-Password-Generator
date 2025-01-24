import repo
from tkinter import ttk, simpledialog, messagebox, Label

class ManagerFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master_password = None
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
        self.password_table = ttk.Treeview(self, columns=("what_for", "uname", "em_addr", "password", "delete"),
                                           show="headings")
        self.password_table.heading("what_for", text="Purpose")
        self.password_table.heading("uname", text="Username")
        self.password_table.heading("em_addr", text="Email")
        self.password_table.heading("password", text="Password")
        self.password_table.heading("delete")  # Heading for the delete column

        # Set column widths
        self.password_table.column("what_for", width=100, anchor="center")
        self.password_table.column("uname", width=100, anchor="center")
        self.password_table.column("em_addr", width=130, anchor="center")
        self.password_table.column("password", width=100, anchor="center")
        self.password_table.column("delete", width=70, anchor="center")

        self.password_table.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

        # Add a scrollbar to the table
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.password_table.yview)
        self.password_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky="ns")

        # Configure tags for the delete button
        self.password_table.tag_configure("delete", foreground="red", font=("Arial", 10, "bold"))

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.refresh_table()
        self.authenticate()

    def authenticate(self):
        check_password = simpledialog.askstring("Authenticate", "You need administrator permissions to view your passwords:", parent=self)
        if check_password is None:
            return
        if check_password.strip():
            self.vault_name = repo.get_vault_name()
            key_salt = repo.authenticate(self.vault_name, check_password)
            if key_salt:
                messagebox.showinfo("Authentication Successful", "You have successfully authenticated to your vault.")
                self.master_password = check_password.strip()
                self.load_passwords()
            else:
                messagebox.showerror("Authentication Failed", "Please check your credentials and try again.")
                return # Exit the function if authentication failed

    def refresh_table(self):
        # Clear existing entries in the table
        for item in self.password_table.get_children():
            self.password_table.delete(item)

    # Update the load_passwords function to insert a "Delete" button
    def load_passwords(self):
        passwords = repo.retrieve_all_passwords(self.master_password, self.vault_name)
        for pwd in passwords:
            # Insert password data into the table with "Delete" in the last column
            self.password_table.insert("", "end", values=(*pwd, "Delete"))

        # Bind the click event to the Treeview
        self.password_table.bind("<Button-1>", self.on_delete_click)

    def on_delete_click(self, event):
        # Identify the row and column where the user clicked
        row_id = self.password_table.identify_row(event.y)
        column = self.password_table.identify_column(event.x)

        if row_id and column == "#5":  # Check if the click was in the "Delete" column
            # Retrieve the "what_for" value from the row
            values = self.password_table.item(row_id, "values")
            if values and len(values) > 0:
                what_for = values[0]  # First column value (e.g., "What For")

                # Prompt for authentication
                check_password = simpledialog.askstring("Authenticate", "You need administrator permission to delete:", parent=self)
                if check_password is None:
                    return  # Cancel if no input

                # Verify the password
                key_salt = repo.authenticate(self.vault_name, check_password)
                if key_salt:
                    # Delete the password after successful authentication
                    repo.delete_password(what_for)
                    self.refresh_table()
                    self.load_passwords()
                    messagebox.showinfo("Success", f"The password for '{what_for}' has been deleted.")
                else:
                    # Show error if authentication fails
                    messagebox.showerror("Authentication Failed", "Incorrect password. Deletion aborted.")