import sqlite3
import hashlib
import db_constants
import aes
import generator

def exists_vault():
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.EXISTS_VAULT)
        count = cursor.fetchone()[0]

        return count != 0

def get_vault_name():
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.GET_VAULT_NAME)
        vault_name = cursor.fetchone()[0]

    return vault_name

def create_vault(vault_name):
    password = generator.generate_bbs_password(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-_?")

    hashed_pw = aes.hash_password(password)
    salt = generator.generate_bbs_salt()

    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.CREATE_VAULT, (vault_name, hashed_pw, salt))

    return password


def authenticate(vault, password):
    password = password.encode()
    hashed_password = hashlib.sha256(password).hexdigest()

    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.GET_HASH, (vault,))
        hash_from_db = cursor.fetchone()[0]

    if hashed_password == hash_from_db:
        return True
    return False


def retrieve_all_passwords(mpw, vault):
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.RETRIEVE_ALL_PASSWORDS)
        passwords = cursor.fetchall()

    salt = retrieve_e_k_s(vault)
    decrypted_passwords = []
    decryption_key = aes.derive_encryption_key(mpw, salt)

    for pwd in passwords:
        decr = aes.decrypt_aes(pwd[3], decryption_key)
        new_pwd = (pwd[0], pwd[1], pwd[2], decr)
        decrypted_passwords.append(new_pwd)

    return decrypted_passwords


def create_new_password(vault, mpw, what_for, password, uname=None, em_addr=None):

    salt = retrieve_e_k_s(vault)
    encryption_key = aes.derive_encryption_key(mpw, salt)
    encrypted_pw = aes.encrypt_aes(password, encryption_key)

    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.CREATE_PASSWORD, (what_for, uname, em_addr, encrypted_pw))


def retrieve_e_k_s(vault_name):
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.GET_E_K_S, (vault_name,))
        e_k_s = cursor.fetchone()[0]

    return e_k_s

def delete_password(what_for):
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.DELETE_PASSWORD, (what_for,))

def create_tables():
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.CREATE_VAULT_TABLE)
        cursor.execute(db_constants.CREATE_PW_TABLE)
