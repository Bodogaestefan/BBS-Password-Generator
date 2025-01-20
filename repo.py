import sqlite3
import hashlib
import db_constants


def exists_vault():
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.EXISTS_VAULT)
        count = cursor.fetchone()[0]

        return count != 0


def create_vault(vault_name, mpw_hs, e_k_s):
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.CREATE_VAULT, (vault_name, mpw_hs, e_k_s))


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


def retrieve_all_passwords():
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.RETRIEVE_ALL_PASSWORDS)
        passwords = cursor.fetchall()

    return passwords


def create_new_password(what_for, password, uname=None, em_addr=None):
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(db_constants.CREATE_PASSWORD, (what_for, uname, em_addr, password))


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
