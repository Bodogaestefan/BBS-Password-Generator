import base64
import repo, generator, aes
import tkinter as tk
from tkinter import ttk

def exists_vault():
    return repo.exists_vault()

def create_vault(vault_name):
    # if no vault exists, generate password for vault, hash pw, generate salt
    # create vault record: vault_name, password_hash, generated_salt
    password = generator.generate_bbs_password(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-_?")

    hashed_pw = aes.hash_password(password)
    salt = generator.generate_bbs_salt()

    repo.create_vault(vault_name, hashed_pw, salt)
    return password


def authenticate(vault, password):
    # attempts to authenticate, if success returns encryption_key_salt
    if repo.authenticate(vault, password):
        return repo.retrieve_e_k_s(vault)
    return False


def retrieve_all_passwords(mpw, vault=None):
    passwords = repo.retrieve_all_passwords()
    salt = repo.retrieve_e_k_s(vault)
    decrypted_passwords = []
    decryption_key = aes.derive_encryption_key(mpw, salt)


    for pwd in passwords:
        decr = aes.decrypt_aes(pwd[3], decryption_key)
        new_pwd = (pwd[0], pwd[1], pwd[2], decr)
        decrypted_passwords.append(new_pwd)


def create_password(vault, mpw, what_for, password, uname, em_addr):
    salt = repo.retrieve_e_k_s(vault)
    encryption_key = aes.derive_encryption_key(mpw, salt)
    encrypted_pw = aes.encrypt_aes(password, encryption_key)
    repo.create_new_password(what_for, encrypted_pw, uname, em_addr)


class ManagerFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Add content
        label = ttk.Label(self, text="Password Manager", font=("Arial", 18))
        label.grid(row=0, column=0, pady=20, sticky="n")

        text = ttk.Label(self, text="Store and manage your passwords securely here.",
                        font=("Arial", 12), wraplength=500, justify="center")
        text.grid(row=1, column=0, pady=10, sticky="n")

        # Example of adding saved passwords (in memory for simplicity)
        self.password_list = tk.Listbox(self, font=("Arial", 12), width=40, height=8)
        self.password_list.grid(row=2, column=0, pady=10, padx=20, sticky="n")

        add_button = ttk.Button(self, text="Add Example Password",
                               command=self.add_example_password)
        add_button.grid(row=3, column=0, pady=10, sticky="n")

    def add_example_password(self):
        self.password_list.insert("end", "example@password123")


