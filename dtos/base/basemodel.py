import json
from typing import TypeVar, Type, Generic, Dict, Any

from includes.logger import get_logger
from pydantic import BaseModel, ValidationError, RootModel

log = get_logger()

T_MyBaseModel = TypeVar('T_MyBaseModel', bound='MyBaseModel')
T_MyRootModel = TypeVar('T_MyRootModel', bound='MyRootModel')


class LoadModel:
    @classmethod
    def load(cls: Type[T_MyBaseModel], data) -> T_MyBaseModel:
        """Auto-detects and switches+validates loading another BaseModel, json, or a dict"""

        # If it's an instance of BaseModel, we json dump it
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


class MyBaseModel(LoadModel, BaseModel):
    class Config:
        # Enforce strict types for better debugging
        strict_types = True


class MyRootModel(Generic[T_MyRootModel], LoadModel, RootModel[T_MyRootModel]):
    # Optional: Override methods from RootModel if needed
    def dict(self, *args, **kwargs) -> T_MyRootModel:
        # Use the root property from RootModel to access the data
        return self.root
