import hashlib

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from bcrypt import checkpw
import os


class Cryptographer:
    def __init__(self, filename: str):
        if not os.path.exists(filename):
            self.private_key = self._create_private_key()
            self._save_key(self.private_key, filename)
        else:
            try:
                self.private_key = self._load_key(filename)
            except Exception as e:
                print("Ошибка чтения ключа", e)
                raise e

    def _create_private_key(self):
        print("Создаю новый ключ...")
        return rsa.generate_private_key(
            # Число, двоичное представление которого начинается и кончается с 1 (остальные 0)
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

    def _save_key(self, pk: RSAPrivateKey, filename: str):
        pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(filename, 'wb') as pem_out:
            pem_out.write(pem)

    def _load_key(self, filename):
        with open(filename, 'rb') as pem_in:
            pem_lines = pem_in.read()
        private_key = load_pem_private_key(pem_lines, None, default_backend())
        return private_key

    def get_public_key(self):
        return self.private_key.public_key()

    def encrypt(self, data: str) -> bytes:
        public_key = self.get_public_key()
        return public_key.encrypt(
            data.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt(self, data: bytes) -> str:
        decrypted_data = self.private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data.decode()

    @staticmethod
    def make_hash(data: str) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @staticmethod
    def check_hash(data: str, hashed_data: str) -> bool:
        return checkpw(data.encode("utf-8"), hashed_data.encode("utf-8"))


if __name__ == "__main__":
    # c = Cryptographer("private_key.pem")
    # message = "Супер секрет"
    # encrypted = c.encrypt(message)
    # print(encrypted)
    # decrypted = c.decrypt(encrypted)
    # print(decrypted)

    password = "dsfsdfsdfsdqwertydwdqwdqwdqwdqwvefewfedsfsgwefsdwdwefdsfewfscvbvcbdfdfgfdgdfwef"
    hashed = Cryptographer.make_hash(password)
    print(hashed, len(hashed))
    print(Cryptographer.check_hash(password, hashed))
