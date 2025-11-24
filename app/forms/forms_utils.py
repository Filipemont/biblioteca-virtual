import re
from wtforms.validators import ValidationError


class FormsUtils:
    @staticmethod
    def validate_password(password):
        password_value = password.data

        errors = []

        if len(password_value) < 8:
            errors.append('A senha deve ter pelo menos 8 caracteres.')

        if not re.search(r'[A-Z]', password_value):
            errors.append('A senha deve conter pelo menos uma letra maiúscula.')

        if not re.search(r'[a-z]', password_value):
            errors.append('A senha deve conter pelo menos uma letra minúscula.')

        if not re.search(r'[0-9]', password_value):
            errors.append('A senha deve conter pelo menos um número.')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password_value):
            errors.append('A senha deve conter pelo menos um caractere especial (!@#$%^&*()).')

        delimiter = "<br>"
        if len(errors) > 0:
            raise ValidationError(delimiter.join(errors))
