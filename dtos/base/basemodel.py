import json
from collections.abc import Callable
from typing import TypeVar, Type, get_args, List, Generic, Any

from pydantic.main import IncEx
from typing_extensions import get_origin

from includes.logger import get_logger
from pydantic import BaseModel, ValidationError, Field

from includes.types import JSONType

log = get_logger()

# Allows preserving autocomplete via the load method return
T = TypeVar('T', bound='MyBaseModel')
PydanticUndefined = None # Needed to define here for json() override

class MyBaseModel(BaseModel):
    class Config:
        # Enforce strict types for better debugging
        strict_types = True
        arbitrary_types_allowed = True  # Allow things like Collections/Restricted Collections in properties

    def to_list(self) -> List[str | int | float]:
        # Use model_dump to get all attribute values as a list, keeping DRY
        return list(self.model_dump().values())

    def json(
        self,
        *,
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]
        models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]
        **dumps_kwargs: Any,) -> str:
        return super().model_dump_json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

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
