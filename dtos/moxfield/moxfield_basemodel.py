import config
import os
import sys
from typing import TypeVar, Type, Generic
from includes.logger import get_logger, setup_logger
from pydantic import PrivateAttr, RootModel

from includes.types import JSONType
from includes.utils import display_friendly_error
from dtos.base.basemodel import MyBaseModel

log = get_logger()

# Allows preserving autocomplete via the load method return
T_Mox = TypeVar('T_Mox', bound='MoxFieldBaseModel')


class MoxFieldBaseModel(MyBaseModel):
    _friendly_errors: bool = PrivateAttr(default=False)

    @classmethod
    def load(cls: Type[T_Mox], data) -> MyBaseModel | T_Mox:
        cls.set_friendly_errors(os.getenv('FRIENDLY_ERRORS') == '1')
        try:
            return super().load(data)
        except Exception as e:
            # Log the technical error
            log.error(config.MoxFieldErrors.ERROR_MSG, exc_info=e)

            # Handle user-friendly error message in local mode
            if cls._friendly_errors:
                display_friendly_error(config.MoxFieldErrors.FRIENDLY_ERROR_MSG)
                # Exit since we are in pretty error mode and dont want to print stack trace
                sys.exit(1)
            # Re-raise the exception to keep normal behavior
            raise

    @classmethod
    def set_friendly_errors(cls, value: bool):
        cls._friendly_errors = value
        setup_logger(local_mode=value)


T_JSONType = TypeVar('T_JSONType', bound=JSONType)


# Create a generic root model that extends MoxFieldBaseModel and RootModel
class MyMoxRootModel(RootModel[T_JSONType], MoxFieldBaseModel, Generic[T_JSONType]):
    @classmethod
    def load(cls, data) -> 'MyMoxRootModel':
        """Override load method to include custom error handling logic."""
        cls.set_friendly_errors(os.getenv('FRIENDLY_ERRORS') == '1')
        try:
            # Call the load method from MoxFieldBaseModel
            return super().load(data)
        except Exception as e:
            # Handle errors similarly to MoxFieldBaseModel
            log.error("Error occurred while loading data in MyMoxRootModel.", exc_info=e)

            if cls._friendly_errors:
                # Display a friendly error message
                print("Friendly error message from MyMoxRootModel.")
                sys.exit(1)
            raise
