def caesar_encrypt_file(input_file, output_file, key):
    with open(input_file, "rb") as f:
        file_data = f.read()

    encrypted_data = bytes((byte + key) % 256 for byte in file_data)

    with open(output_file, "wb") as f:
        f.write(encrypted_data)

def caesar_decrypt_file(input_file, output_file, key):
    with open(input_file, "rb") as f:
        file_data = f.read()

    decrypted_data = bytes((byte - key) % 256 for byte in file_data)

    with open(output_file, "wb") as f:
        f.write(decrypted_data)
