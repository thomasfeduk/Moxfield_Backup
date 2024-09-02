import re
from typing import Any, Dict, List

from debug import *


class InvalidFilenameError(Exception):
    pass


def safe_filename(filename: str) -> str:
    safe_name = re.sub(r'[^a-zA-Z0-9-_ ]', '', filename)
    safe_name = safe_name.strip()
    if safe_name == '':
        raise InvalidFilenameError(f'Filename is invalid as it resulted in zero acceptable characters.\n'
                                   f'Original passed value: "{filename}"')
    return safe_name


def is_json_compatible(data: Any) -> bool:
    # Tuple of all allowed JSON-compatible types
    allowed_types = (Dict, List, str, int, float, bool, type(None))

    # Use isinstance to check if data is not of any allowed types
    return isinstance(data, allowed_types)


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
