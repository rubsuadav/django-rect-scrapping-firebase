import re


def validate_register(name, last_name, phone, email, password):
    email_regex = r'^\w+([.-]?\w+)*@(gmail|hotmail|outlook)\.com$'
    phone_regex = r'^(\+34|0034|34)?[ -]*(6|7)[ -]*([0-9][ -]*){8}$'
    # (?=.*?[#?!@$%^&*-]) para que tenga al menos un caracter especial
    password_pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$'

    if len(name) < 3:
        raise ValueError('nombre debe tener más de 3 caracteres')

    if len(last_name) < 3:
        raise ValueError('apellido debe tener más de 3 caracteres')

    if not re.match(email_regex, email):
        raise ValueError(
            'email inválido, debe de ser de gmail, hotmail o outlook')

    if not re.match(phone_regex, phone):
        raise ValueError(
            'número de teléfono móvil inválido, debe de ser de españa')

    if not re.match(password_pattern, password):
        raise ValueError(
            'contraseña debe contener al menos una mayúscula, una minúscula, un número, un caracter especial y debe tener más de 6 caracteres')
