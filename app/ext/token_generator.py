from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer  # type: ignore


class TokenGenerator:
    __safe: object | None = None

    @staticmethod
    def init_app(app) -> None:
        TokenGenerator.__safe = URLSafeTimedSerializer(app.secret_key)

    @staticmethod
    def get_token(object: object, salt: str) -> str:
        return TokenGenerator.__safe.dumps(object, salt=salt)

    @staticmethod
    def loads(token: str, salt: str, max_age: int) -> dict | str:
        try:
            return TokenGenerator.__safe.loads(token, salt=salt, max_age=max_age)
        except (BadSignature, SignatureExpired):
            return None
