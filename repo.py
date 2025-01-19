import sqlite3
import hashlib

EXISTS_VAULT = '''
    SELECT COUNT(*) FROM main.vault;
'''

CREATE_VAULT = '''
    INSERT INTO main.vault (vault_name, mpw_hs, e_k_s) VALUES (?,?,?);
'''

GET_HASH = '''
    SELECT mpw_hs FROM main.vault WHERE vault_name = ?;
'''
GET_E_K_S = '''
    SELECT e_k_s FROM main.vault WHERE vault_name = ?;
'''

RETRIEVE_ALL_PASSWORDS = '''
    SELECT * FROM main.vault_pws;
'''

CREATE_PASSWORD = '''
    INSERT INTO main.vault_pws (what_for, uname, em_addr, e_pwd) VALUES (?,?,?,?)
'''


def exists_vault():
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(EXISTS_VAULT)
        count = cursor.fetchone()[0]

        return count != 0  # Returns True if there is at least one record, False otherwise


def create_vault(vault_name, mpw_hs, e_k_s):
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(CREATE_VAULT, (vault_name, mpw_hs, e_k_s))


def authenticate(vault, password):
    password = password.encode()
    hashed_password = hashlib.sha256(password).hexdigest()

    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(GET_HASH, (vault,))
        hash_from_db = cursor.fetchone()[0]

    print(hashed_password)
    print(hash_from_db)
    if hashed_password == hash_from_db:
        return True
    return False


def retrieve_all_passwords():
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_ALL_PASSWORDS)
        passwords = cursor.fetchall()

    return passwords


def create_new_password(what_for, password, uname=None, em_addr=None):
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(CREATE_PASSWORD, (what_for, uname, em_addr, password))


def retrieve_e_k_s(vault_name):
    with sqlite3.connect("../pw_mng.db") as connection:
        cursor = connection.cursor()
        cursor.execute(GET_E_K_S, (vault_name,))
        e_k_s = cursor.fetchone()[0]

    return e_k_s
