import os
import getpass
from crypto_utils import generate_salt, derive_key, encrypt_data, decrypt_data


VAULT_DIR = "vault_storage"


def initialize_vault():
    # Create vault directory if it does not exist
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR)


def store_file(filepath: str):
    # Store and encrypt a file inside the vault
    password = getpass.getpass("Enter vault password: ")
    salt = generate_salt()
    key = derive_key(password, salt)

    with open(filepath, "rb") as f:
        data = f.read()

    encrypted_data = encrypt_data(data, key)

    filename = os.path.basename(filepath)
    vault_path = os.path.join(VAULT_DIR, filename + ".vault")

    with open(vault_path, "wb") as f:
        # Store salt + encrypted data
        f.write(salt + encrypted_data)

    print("File successfully encrypted and stored in vault.")


def retrieve_file(filename: str):
    # Decrypt and retrieve a file from the vault
    password = getpass.getpass("Enter vault password: ")

    vault_path = os.path.join(VAULT_DIR, filename + ".vault")

    with open(vault_path, "rb") as f:
        file_data = f.read()

    salt = file_data[:16]
    encrypted_data = file_data[16:]

    key = derive_key(password, salt)

    try:
        decrypted_data = decrypt_data(encrypted_data, key)

        output_path = "decrypted_" + filename
        with open(output_path, "wb") as f:
            f.write(decrypted_data)

        print("File successfully decrypted:", output_path)
    except Exception:
        print("Invalid password or corrupted file.")


def main():
    initialize_vault()

    print("ShadowVault CLI")
    print("1 - Store file")
    print("2 - Retrieve file")

    choice = input("Choose an option: ")

    if choice == "1":
        path = input("Enter file path: ")
        store_file(path)
    elif choice == "2":
        filename = input("Enter filename (without .vault): ")
        retrieve_file(filename)
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
