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
