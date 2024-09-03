import json
from typing import TypeVar, Type, get_args, List, Generic

from typing_extensions import get_origin

from includes.logger import get_logger
from pydantic import BaseModel, ValidationError, Field

from includes.types import JSONType

log = get_logger()

# Allows preserving autocomplete via the load method return
T = TypeVar('T', bound='MyBaseModel')


class MyBaseModel(BaseModel):
    # class Config:
    #     # Enforce strict types for better debugging
    #     strict_types = True

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

        # Ensure the input is a valid JSON-compatible type
        json_types = get_args(JSONType)  # Retrieve the component types from JSONType

        # Ensure the input is a valid JSON-compatible type
        json_types = get_args(JSONType)  # Retrieve the component types from JSONType

        # Check if the data is one of the acceptable types using origins
        if not any(isinstance(data, get_origin(t) or t) for t in json_types):
            log.error("Input data must be a valid JSON-compatible type.", exc_info=True)
            raise TypeError("Input data must be a valid JSON-compatible type.")

        # Determine how to instantiate the model
        if isinstance(data, dict):
            try:
                # Attempt to unpack the dictionary into the model's fields
                return cls(**data)
            except ValidationError as e:
                log.error("Validation error occurred while unpacking data into model fields.", exc_info=e)
                raise
        # Use root instantiation for all other JSON-compatible types
        return cls(root=data)  # Use root keyword for RootModel instantiation
