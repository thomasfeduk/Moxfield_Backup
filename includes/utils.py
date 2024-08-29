import re


class InvalidFilenameError(Exception):
    pass


def safe_filename(filename: str) -> str:
    safe_name = re.sub(r'[^a-zA-Z0-9-_ ]', '', filename)
    safe_name = safe_name.strip()
    if safe_name == '':
        raise InvalidFilenameError(f'Filename is invalid as it resulted in zero acceptable characters.\n'
                                   f'Original passed value: "{filename}"')
    return safe_name


def display_friendly_error(friendly_error_msg: str) -> None:
    cols = 85
    print('\n')
    print('-' * cols)
    print('!' * cols)
    print('-' * cols)
    print('\n')
    print(friendly_error_msg)
    print('\n')
    print('-' * cols)
    print('!' * cols)
    print('-' * cols)
