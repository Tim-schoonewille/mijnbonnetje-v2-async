from humps import camelize


def to_camel(string: str) -> str:
    return camelize(string)


def check_password_requirements(cls, value):
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not any(char.isupper() for char in value):
        raise ValueError("Password must contain at least 1 capital letter.")
    if not any(char.isdigit() for char in value):
        raise ValueError("Password must contain at least 1 digit.")
    if not any(char in r"!@#$%&?" for char in value):
        raise ValueError("Password must contain at least 1 special character.")
    return value
