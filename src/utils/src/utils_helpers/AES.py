from cryptography.fernet import Fernet
import os


def get_aes_secret_key():
    aes_secret_key_path = os.getenv('AES_SECRET_KEY_FILE')
    with open(aes_secret_key_path, 'rb') as f:
        return f.read()


AES_SECRET_KEY = get_aes_secret_key()
fernet = Fernet(AES_SECRET_KEY)


def encrypt_data(data: str) -> str:
    encrypted_data = fernet.encrypt(data.encode('utf-8'))
    return encrypted_data.decode('utf-8')


def decrypt_data(encrypted_data: str) -> str:
    decrypted_data = fernet.decrypt(encrypted_data.encode('utf-8'))
    return decrypted_data.decode('utf-8')
