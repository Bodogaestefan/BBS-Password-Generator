from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib


def pad(text):
    padder = padding.PKCS7(256).padder()
    padded_text = padder.update(text) + padder.finalize()
    return padded_text


def unpad(padded_plaintext):
    padding_length = padded_plaintext[-1]
    return padded_plaintext[:-padding_length]


def hash_password(password):
    password = password.encode()
    return hashlib.sha256(password).hexdigest()


def derive_encryption_key(password, salt):
    password_bytes = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10
    )
    derived_key = kdf.derive(password_bytes)

    return derived_key


def encrypt_aes(plaintext, key):
    plaintext = plaintext.encode()
    plaintext = pad(plaintext)
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext


def decrypt_aes(ciphertext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadded_plaintext = unpad(padded_plaintext)

    return unpadded_plaintext.decode()
