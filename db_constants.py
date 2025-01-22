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

DELETE_PASSWORD = '''
    DELETE FROM main.vault_pws WHERE what_for = ?;
'''

CREATE_VAULT_TABLE = '''
    CREATE TABLE IF NOT EXISTS vault (
        vault_name TEXT PRIMARY KEY,
        mpw_hs TEXT,
        e_k_s TEXT
    );
'''

CREATE_PW_TABLE = '''
    CREATE TABLE IF NOT EXISTS vault_pws (
        what_for TEXT,
        uname TEXT,
        em_addr TEXT,
        e_pwd BLOB
    );
'''

GET_VAULT_NAME = '''
    SELECT vault_name FROM main.vault;
'''
