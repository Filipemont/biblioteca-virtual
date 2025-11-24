import base64
import io
import os
import tink  # type: ignore
from tink import aead, cleartext_keyset_handle, daead  # type: ignore


class DataEncrypt:
    __secret_key: str | None = None
    __aead_primitive: str | None = None
    __daead_primitive: str | None = None

    @staticmethod
    def __keyset_aead_by_env() -> str:
        keyset_base64: str = os.getenv("TINK_KEYSET_AEAD")
        if not keyset_base64:
            raise ValueError("Chave TINK_KEYSET_AEAD não definida na variável de ambiente")
        keyset_str: str = base64.b64decode(keyset_base64).decode('utf-8')
        return cleartext_keyset_handle.read(tink.JsonKeysetReader(keyset_str))

    @staticmethod
    def __keyset_daead_by_env() -> str:
        keyset_base64: str = os.getenv("TINK_KEYSET_DAEAD")
        if not keyset_base64:
            raise ValueError("Chave TINK_KEYSET_DAEAD não definida na variável de ambiente")
            # Decodificar a chave base64 e ler o keyset
        keyset_str: str = base64.b64decode(keyset_base64).decode('utf-8')
        return cleartext_keyset_handle.read(tink.JsonKeysetReader(keyset_str))

    @staticmethod
    def init(secret_key: str):
        DataEncrypt.__secret_key = secret_key
        aead.register()
        daead.register()

        keyset_handle_aead: str = DataEncrypt.__keyset_aead_by_env()
        DataEncrypt.__aead_primitive: str = keyset_handle_aead.primitive(aead.Aead)

        keyset_handle_daead: str = DataEncrypt.__keyset_daead_by_env()
        DataEncrypt.__daead_primitive: str = keyset_handle_daead.primitive(daead.DeterministicAead)

    @staticmethod
    def get_encrypted_aead(data) -> str:
        data_encripted: str = DataEncrypt.__aead_primitive.encrypt(data.encode(), DataEncrypt.__secret_key.encode())
        return base64.b64encode(data_encripted).decode('utf-8')

    @staticmethod
    def get_decrypted_aead(data) -> str:
        data_encrypted: str = base64.b64decode(data)
        return DataEncrypt.__aead_primitive.decrypt(data_encrypted, DataEncrypt.__secret_key.encode()).decode('utf-8')

    @staticmethod
    def get_encrypted_daead(data) -> str:
        data_encripted: str = DataEncrypt.__daead_primitive.encrypt_deterministically(
            data.encode(), DataEncrypt.__secret_key.encode()
        )
        return base64.b64encode(data_encripted).decode('utf-8')

    @staticmethod
    def get_decrypted_daead(data) -> str:
        data_encrypted: str = base64.b64decode(data)
        return DataEncrypt.__daead_primitive.decrypt_deterministically(
            data_encrypted, DataEncrypt.__secret_key.encode()
        ).decode('utf-8')
