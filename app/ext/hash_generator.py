import bcrypt  # type: ignore


class HashGenerator:
    @staticmethod
    def generate_hashed_password(password: str) -> tuple:
        salt: bytes = bcrypt.gensalt()
        hashed_password: bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
        return salt, hashed_password

    def get_hashed_password(password: str, salt: str):
        salt_bytes: bytes = bytes(salt)
        hashed_password: bytes = bcrypt.hashpw(password.encode('utf-8'), salt_bytes)
        return hashed_password.decode('utf-8')
