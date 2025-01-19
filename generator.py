import secrets
import tkinter as tk
from tkinter import ttk

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_large_prime():
    while True:
        num = secrets.randbelow(10 ** 10 - 10 ** 9) + 10 ** 9
        if is_prime(num):
            return num


def generate_blum_blum_shub_bit_sequence(bits):
    p = generate_large_prime()
    q = generate_large_prime()
    while p == q:
        q = generate_large_prime()

    n = p * q
    seed = secrets.randbelow(n)
    x = seed * seed % n

    random_bits = []
    for _ in range(bits):
        x = x * x % n
        random_bits.append(x % 2)

    return random_bits


def generate_bbs_password(password_alphabet, password_length=32):
    random_bits = generate_blum_blum_shub_bit_sequence(password_length * 8)

    password = ''.join(
        password_alphabet[int(''.join(map(str, random_bits[i * 8:(i + 1) * 8])), 2) % len(password_alphabet)] for i
        in range(password_length))

    return password


def generate_bbs_salt():
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-_?"
    random_bits = generate_blum_blum_shub_bit_sequence(16 * 8)

    salt = ''.join(
        alphabet[int(''.join(map(str, random_bits[i * 8:(i + 1) * 8])), 2) % len(alphabet)] for i
        in range(16))

    return salt.encode()


class GeneratorFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Configure grid layout
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # Title label
        label = ttk.Label(self, text="Password Generator", font=("Arial", 18))
        label.grid(row=0, column=1, pady=20, sticky="n")

        # Password length input
        length_label = ttk.Label(self, text="Password Length: ", font=("Arial", 12))
        length_label.grid(row=1, column=1, pady=10, sticky="n")

        self.length_var = tk.IntVar(value=8)
        length_entry = ttk.Entry(self, textvariable=self.length_var, font=("Arial", 12), width=5)
        length_entry.grid(row=2, column=1, pady=5, sticky="n")

        # Character type selectors
        checkbox_frame = ttk.Frame(self)
        checkbox_frame.grid(row=3, column=1, pady=10, sticky="n")
        checkbox_frame.grid_columnconfigure((0, 1), weight=1)

        # Character type selectors
        self.include_lowercase = tk.BooleanVar(value=False)
        self.include_uppercase = tk.BooleanVar(value=False)
        self.include_digits = tk.BooleanVar(value=False)
        self.include_special = tk.BooleanVar(value=False)

        ttk.Checkbutton(checkbox_frame, text="Include Lowercase", variable=self.include_lowercase).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(checkbox_frame, text="Include Uppercase", variable=self.include_uppercase).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(checkbox_frame, text="Include Digits", variable=self.include_digits).grid(row=0, column=1, sticky="w")
        ttk.Checkbutton(checkbox_frame, text="Include Special Characters", variable=self.include_special).grid(row=1, column=1, sticky="w")

        # Generated password display
        password_label = ttk.Label(self, text="Generated Password: ", font=("Arial", 12))
        password_label.grid(row=4, column=1, pady=10, sticky="n")

        self.password_var = tk.StringVar()
        password_display = ttk.Entry(self, textvariable=self.password_var, font=("Arial", 12), width=30, state="readonly")
        password_display.grid(row=5, column=1, pady=5, sticky="n")

        button_frame = ttk.Frame(self)
        button_frame.grid(row=6, column=1, pady=10, sticky="n")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        generate_button = ttk.Button(button_frame, text="Generate Password", command=self.generate_password)
        generate_button.grid(row=0, column=0, padx=5)

        save_button = ttk.Button(button_frame, text="Save Password", command=self.save_password)
        save_button.grid(row=0, column=1, padx=5)

    def generate_password(self):
        # Collect selected character types
        password_characters = ""
        if self.include_lowercase.get():
            password_characters += "abcdefghijklmnopqrstuvwxyz"
        if self.include_uppercase.get():
            password_characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.include_digits.get():
            password_characters += "0123456789"
        if self.include_special.get():
            password_characters += "!@#$%^&*()"

        if not password_characters:
            self.password_var.set("Select at least one character type")
            return

        password_length = self.length_var.get()
        if password_length <= 0:
            self.password_var.set("Invalid length")
            return

        # Generate enough random bits for the password
        random_bits = generate_blum_blum_shub_bit_sequence(password_length * 8)

        password = ''.join(
            password_characters[int(''.join(map(str, random_bits[i * 8:(i + 1) * 8])), 2) % len(password_characters)]
            for i in range(password_length))

        self.password_var.set(password)

    def save_password(self):
        # Placeholder for saving password to a file or database
        pass