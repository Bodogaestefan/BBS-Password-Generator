from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib


def hash_password(password):
    password = password.encode()
    return hashlib.sha256(password).hexdigest()


def derive_encryption_key(password, salt):
    """
    Derives the private key from the password using PBKDF2 with HMAC-SHA256.
    """

    password_bytes = password.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # Use SHA-256 as the underlying hash function
        length=32,  # Length of the derived key (32 bytes = 256 bits for AES-256)
        salt=salt,
        iterations=10
    )

    # Derive the key
    derived_key = kdf.derive(password_bytes)

    return derived_key


# AES encryption function
def encrypt_aes(plaintext, key):
    # Convert plaintext to bytes
    plaintext = plaintext.encode()

    # Add PKCS7 padding
    padder = padding.PKCS7(256).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    # Create AES cipher in ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()

    # Encrypt the plaintext
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return ciphertext


# AES decryption function
def decrypt_aes(ciphertext, key):
    # Create AES cipher in ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove PKCS7 padding
    unpadded_plaintext = unpad(padded_plaintext)
    return unpadded_plaintext.decode()


def unpad(padded_plaintext):
    padding_length = padded_plaintext[-1]  # Get the last byte value
    return padded_plaintext[:-padding_length]
