from dataclasses import dataclass

@dataclass(frozen=True)
class Errors:
    LOG_FILE = 'errors.log'  # None if no local logging


@dataclass(frozen=True)
class MoxFieldErrors:
    API_FRIENDLY_ERRORS = True  # If false, show the raw error output when Moxfield API compatability breaks
    ERROR_MSG: str = 'Unexpected response from MoxField API. Spec may have changed.'
    FRIENDLY_ERROR_MSG: str = 'Received an unexpected response from MoxField API. The spec may have changed.' \
                              'Contact Thomas :(\nYou can find more information in errors.log '


@dataclass(frozen=True)
class MoxFieldAPI:
    BASE_URL = "https://api2.moxfield.com"
