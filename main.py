import mariadb
import sys
from CaesarCrypt import *
import os

# Configurare conexiune la MariaDB
def connect_db():
    try:
        conn = mariadb.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            port=3306,
            database="crypto"
        )
        
        if conn:
            print("Conexiunea la baza de date a fost realizată cu succes!")
        else:
            print("Conexiunea la baza de date a eșuat!")
        
        return conn
    except mariadb.Error as e:
        print(f"Eroare la conectare: {e}")
        sys.exit(1)

# Funcții CRUD

# CREATE
def insert_key(algorithm, key_data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO encryption_keys (algorithm, key_data) VALUES (?, ?)", (algorithm, key_data))
    conn.commit()
    conn.close()

def insert_file(file_name, algorithm, key_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO encrypted_files (file_name, algorithm, key_id)
    VALUES (?, ?, ?)""", (file_name, algorithm, key_id))
    conn.commit()
    conn.close()

def insert_performance(file_id, encryption_time, decryption_time, memory_usage):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO performance_logs (file_id, encryption_time, decryption_time, memory_usage)
    VALUES (?, ?, ?, ?)""", (file_id, encryption_time, decryption_time, memory_usage))
    conn.commit()
    conn.close()

# READ
def get_all_keys():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM encryption_keys")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_files():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM encrypted_files")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_performance_logs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM performance_logs")
    rows = cursor.fetchall()
    conn.close()
    return rows

# UPDATE
def update_key(key_id, new_algorithm, new_key_data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE encryption_keys 
    SET algorithm = ?, key_data = ? 
    WHERE id = ?""", (new_algorithm, new_key_data, key_id))
    conn.commit()
    conn.close()

def update_file(file_id, new_file_name, new_algorithm, new_key_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE encrypted_files 
    SET file_name = ?, algorithm = ?, key_id = ? 
    WHERE id = ?""", (new_file_name, new_algorithm, new_key_id, file_id))
    conn.commit()
    conn.close()

def update_performance(perf_id, new_encryption_time, new_decryption_time, new_memory_usage):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE performance_logs 
    SET encryption_time = ?, decryption_time = ?, memory_usage = ? 
    WHERE id = ?""", (new_encryption_time, new_decryption_time, new_memory_usage, perf_id))
    conn.commit()
    conn.close()

# DELETE
def delete_key(key_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM encryption_keys WHERE id = ?", (key_id,))
    conn.commit()
    conn.close()

def delete_file(file_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM encrypted_files WHERE id = ?", (file_id,))
    conn.commit()
    conn.close()

def delete_performance(perf_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM performance_logs WHERE id = ?", (perf_id,))
    conn.commit()
    conn.close()

# Testare funcționalitate
def encrypt_and_store_file(file_path, key, key_id):
    file_name = os.path.basename(file_path)
    
    encrypted_path = os.path.join("encrypted-files", f"encrypted_{file_name}")

    caesar_encrypt_file(file_path, encrypted_path, key)

    insert_file(file_name, "Caesar", key_id)

    print(f"File {file_name} encrypted and saved as {encrypted_path} in the database.")

if __name__ == "__main__":
    
    encrypt_and_store_file("/home/david/Proiecte/crypto-management/plain-text-files/file1.txt", 3, 1)
    