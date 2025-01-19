import base64
import repo, generator, aes

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
        print("Pwd from repo: ",base64.b64encode(pwd[3]).decode())
        decr = aes.decrypt_aes(pwd[3], decryption_key)
        new_pwd = (pwd[0], pwd[1], pwd[2], decr)
        print(new_pwd)
        decrypted_passwords.append(new_pwd)


def create_password(vault, mpw, what_for, password, uname, em_addr):
    salt = repo.retrieve_e_k_s(vault)
    encryption_key = aes.derive_encryption_key(mpw, salt)

    encrypted_pw = aes.encrypt_aes(password, encryption_key)

    repo.create_new_password(what_for, encrypted_pw, uname, em_addr)


