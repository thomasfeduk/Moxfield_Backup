import os
from typing import TypeVar, Type

import config
from pydantic import PrivateAttr
from dtos.base.basemodel import MyBaseModel
from includes.logger import get_logger, setup_logger

log = get_logger()

# Allows preserving autocomplete via the load method return
T = TypeVar('T', bound='MoxFieldBaseModel')


class MoxFieldBaseModel(MyBaseModel):
    _friendly_errors: bool = PrivateAttr(default=False)

    @classmethod
    def load(cls: Type[T], data) -> MyBaseModel | T:
        cls.set_friendly_errors(os.getenv('FRIENDLY_ERRORS') == '1')

        # Custom user-facing messages
        error_msg = config.MoxFieldErrors.ERROR_MSG
        friendly_error_msg = config.MoxFieldErrors.FRIENDLY_ERROR_MSG

        try:
            return super().load(data)
        except Exception as e:
            # Log the technical error
            log.error(error_msg, exc_info=e)

            # Handle user-friendly error message in local mode
            if cls._friendly_errors:
                cls._display_friendly_error(friendly_error_msg)
                # Exit since we are in pretty error mode and dont want to print stack trace
                exit(1)
            # Re-raise the exception to keep normal behavior
            raise

    @classmethod
    def set_friendly_errors(cls, value: bool):
        cls._friendly_errors = value
        setup_logger(local_mode=value)

    @staticmethod
    def _display_friendly_error(local_error_msg):
        cols = 85
        print('\n')
        print('-' * cols)
        print('!' * cols)
        print('-' * cols)
        print('\n')
        print(local_error_msg)
        print('\n')
        print('-' * cols)
        print('!' * cols)
        print('-' * cols)
