import os
from typing import TypeVar, Type
import sys
import config
from pydantic import PrivateAttr
from includes.utils import display_friendly_error
from dtos.base.basemodel import MyBaseModel
from includes.logger import get_logger, setup_logger

log = get_logger()

# Allows preserving autocomplete via the load method return
T = TypeVar('T', bound='MoxFieldBaseModel')


class MoxFieldBaseModel(MyBaseModel):
    _friendly_errors: bool = PrivateAttr(default=False)

    @classmethod
    def load(cls: Type[T], data) -> MyBaseModel | T:
        try:
            return super().load(data)
        except Exception as e:
            # Log the technical error
            log.error(config.MoxFieldErrors.ERROR_MSG, exc_info=e)

            # Handle user-friendly error message in local mode
            if config.MoxFieldErrors.API_FRIENDLY_ERRORS:
                display_friendly_error(config.MoxFieldErrors.FRIENDLY_ERROR_MSG)
                # Exit since we are in pretty error mode and dont want to print stack trace
                sys.exit(1)
            # Re-raise the exception to keep normal behavior
            raise

    @classmethod
    def set_friendly_errors(cls, value: bool):
        cls._friendly_errors = value
        setup_logger(local_mode=value)


