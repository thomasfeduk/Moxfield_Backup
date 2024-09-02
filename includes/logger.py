import logging
import config

log = None


def setup_logger(local_mode: bool = False) -> log:
    global log
    if log is not None:
        # Clear existing handlers to allow reconfiguration
        log.handlers = []

    log = logging.getLogger(__name__)
    log.setLevel(logging.ERROR)
    log.setLevel(getattr(logging, config.Errors.LOG_LEVEL, logging.ERROR))  # Default to ERROR if LOG_LEVEL is invalid

    # Create a file handler for logging errors to a file
    file_handler = logging.FileHandler('../errors.log')
    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    # Store the local mode flag in the logger
    log.local_mode = local_mode

    # Only add a StreamHandler (console output) if local_mode is off
    if not local_mode:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)

    # Avoid duplicate logs by disabling propagation
    log.propagate = False

    return log

def get_logger() -> log:
    """Ensures the logger is set up before returning it."""
    if log is None:
        setup_logger()  # Set up with default configuration if not already set
    return log
