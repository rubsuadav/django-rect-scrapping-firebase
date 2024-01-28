import re
from rest_framework.exceptions import ValidationError


email_regex = r'^\w+([.-]?\w+)*@((gmail|hotmail|outlook)\.com|alum\.us\.es)$'
# (?=.*?[#?!@$%^&*-]) para que tenga al menos un caracter especial
password_pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$'


def validate_register(name, last_name, phone, email, password):
    errors = {}
    phone_regex = r'^(\+34|0034|34)?[ -]*(6|7)[ -]*([0-9][ -]*){8}$'

    if len(name) < 3:
        errors['name'] = 'nombre debe tener más de 3 caracteres'

    if len(last_name) < 3:
        errors['last_name'] = 'apellido debe tener más de 3 caracteres'

    if not re.match(email_regex, email):
        errors['email'] = 'email inválido, debe de ser de gmail, hotmail o outlook'

    if not re.match(phone_regex, phone):
        errors['phone'] = 'número de teléfono móvil inválido, debe de ser de españa'

    if not re.match(password_pattern, password):
        errors['password'] = 'contraseña debe contener al menos una mayúscula, una minúscula, un número, un caracter especial y debe tener más de 6 caracteres'

    if errors:
        raise ValidationError(errors)


def validate_login(email, password):
    errors = {}
    if not re.match(email_regex, email):
        errors['email'] = 'email inválido, debe de ser de gmail, hotmail o outlook'

    if not re.match(password_pattern, password):
        errors['password'] = 'contraseña debe contener al menos una mayúscula, una minúscula, un número, un caracter especial y debe tener más de 6 caracteres'

    if errors:
        raise ValidationError(errors)
