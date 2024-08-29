import json
from typing import TypeVar, Type

from includes.logger import get_logger
from pydantic import BaseModel, ValidationError

log = get_logger()

# Allows preserving autocomplete via the load method return
T = TypeVar('T', bound='MyBaseModel')


class MyBaseModel(BaseModel):
    @classmethod
    def load(cls: Type[T], data) -> T:
        """Auto-detects and switches+validates loading another Basemode, json or a dict"""

        # If it's an instance of Basemodel, we json dump it
        if isinstance(data, BaseModel):
            data = data.json()

        # Try to JSON decode
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                # Log and raise the exception, no sys.exit
                log.error("Unexpected error occurred while parsing JSON.", exc_info=e)
                raise

        # Ensure the input is a dictionary
        if not isinstance(data, dict):
            log.error("Input data must be a dictionary or a valid JSON string.", exc_info=True)
            raise TypeError("Input data must be a dictionary or a valid JSON string.")

        # Validate the input data using Pydantic
        try:
            return cls(**data)
        except ValidationError as e:
            log.error("Validation error occurred.", exc_info=e)
            raise
