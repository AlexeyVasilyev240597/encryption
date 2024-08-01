from cryptography.fernet import Fernet
import os

def generate_key() -> bytes:
    """Generates a new encryption key."""
    return Fernet.generate_key()

def encrypt_file_name(file_name: str, key: bytes) -> str:
    """Encrypts the file name using Fernet symmetric encryption."""
    fernet = Fernet(key)
    encrypted_name = fernet.encrypt(file_name.encode()).decode()
    return encrypted_name

def decrypt_file_name(encrypted_name: str, key: bytes) -> str:
    """Decrypts the file name using Fernet symmetric encryption."""
    fernet = Fernet(key)
    decrypted_name = fernet.decrypt(encrypted_name.encode()).decode()
    return decrypted_name

def encrypt_file_content(file_path: str, key: bytes) -> None:
    """Encrypts the content of the file."""
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original_content = file.read()
    
    encrypted_content = fernet.encrypt(original_content)
    
    with open(file_path, 'wb') as file:
        file.write(encrypted_content)

def decrypt_file_content(file_path: str, key: bytes) -> None:
    """Decrypts the content of the file."""
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_content = file.read()
    
    decrypted_content = fernet.decrypt(encrypted_content)
    
    with open(file_path, 'wb') as file:
        file.write(decrypted_content)

def encrypt_files_in_directory(directory_path: str, name_key: bytes, content_key: bytes) -> None:
    """Encrypts all files in the specified directory, preserving folder structure."""
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            full_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(full_path, directory_path)
            encrypted_relative_path = os.path.join(*[encrypt_file_name(part, name_key) for part in relative_path.split(os.sep)])

            # Encrypt file content
            encrypt_file_content(full_path, content_key)

            # Create new directory if it doesn't exist
            new_dir = os.path.join(directory_path, os.path.dirname(encrypted_relative_path))
            os.makedirs(new_dir, exist_ok=True)

            # Rename the file with the encrypted name
            new_full_path = os.path.join(directory_path, encrypted_relative_path)
            os.rename(full_path, new_full_path)

def decrypt_files_in_directory(directory_path: str, name_key: bytes, content_key: bytes) -> None:
    """Decrypts all files in the specified directory, restoring the original folder structure."""
    for root, dirs, files in os.walk(directory_path, topdown=False):  # Process files first
        for file_name in files:
            full_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(full_path, directory_path)
            decrypted_relative_path = os.path.join(*[decrypt_file_name(part, name_key) for part in relative_path.split(os.sep)])

            # Decrypt file content
            decrypt_file_content(full_path, content_key)

            # Create new directory if it doesn't exist
            new_dir = os.path.join(directory_path, os.path.dirname(decrypted_relative_path))
            os.makedirs(new_dir, exist_ok=True)

            # Rename the file with the decrypted name
            new_full_path = os.path.join(directory_path, decrypted_relative_path)
            os.rename(full_path, new_full_path)

# Example usage
name_key = generate_key()
content_key = generate_key()

# Encrypt files
encrypt_files_in_directory('path/to/directory', name_key, content_key)

# Decrypt files
decrypt_files_in_directory('path/to/directory', name_key, content_key)
