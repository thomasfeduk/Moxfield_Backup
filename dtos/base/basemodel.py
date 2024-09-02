import json
from typing import TypeVar, Type, Generic, Dict, Any

from includes.logger import get_logger
from pydantic import BaseModel, ValidationError, RootModel

log = get_logger()

T_LoadModel = TypeVar('T', bound='LoadModel')
T_MyBaseModel = TypeVar('T', bound='MyBaseModel')
T_MyRootModel = TypeVar('T', bound='MyRootModel')


class LoadModel(Generic[T_LoadModel]):
    @classmethod
    def load(cls: Type[T_LoadModel], data) -> T_LoadModel | T_MyBaseModel | T_MyRootModel:
        """Auto-detects and switches+validates loading another BaseModel, JSON, or a dict"""

        # If it's an instance of BaseModel, convert it to JSON string
        if isinstance(data, BaseModel):
            data = data.json()

        # Try to decode a JSON string
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


class MyBaseModel(BaseModel, LoadModel['MyBaseModel']):
    class Config:
        # Enforce strict types for better debugging
        strict_types = True


class MyRootModel(RootModel[T_MyRootModel], LoadModel['MyRootModel']):
    # Add custom methods or properties here if needed

    # Example: Override the dict method to match RootModel behavior
    def dict(self, *args, **kwargs) -> T_MyRootModel:
        # Use the root property from RootModel to access the data
        return self.root
