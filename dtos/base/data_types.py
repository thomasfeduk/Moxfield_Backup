from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from pydantic import StringConstraints
from pydantic_core import core_schema, CoreSchema
from pydantic_core.core_schema import SerializationInfo

# Define your custom types using Annotated
StrPopulated = Annotated[str, StringConstraints(min_length=1, pattern=r'\S+')]
DateYmd = Annotated[str, StringConstraints(pattern=r'^\d{4}-\d{2}-\d{2}$')]


class DatetimeIso8601:
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: type, handler: Callable) -> CoreSchema:
        # Define a schema that validates the input using regex and then parses it to a datetime object
        schema = core_schema.str_schema(
            pattern=r"^\d{4}(-\d{2}(-\d{2}(T\d{2}(:\d{2}(:\d{2}(\.\d{1,6})?)?)?(Z|[+-]\d{2}(:?\d{2})?)?)?)?)?$"
        )

        # Add a custom validator function that converts the validated string to a datetime object
        validation_schema = core_schema.with_info_after_validator_function(
            cls.parse_datetime, schema
        )

        # Combine validation with serialization using `core_schema.general_after_validator_function`
        return core_schema.general_after_validator_function(
            cls.serialize_datetime, validation_schema
        )

    @classmethod
    def parse_datetime(cls, value: str, info: core_schema.ValidationInfo) -> datetime:
        if isinstance(value, datetime):
            return value
        try:
            # Convert the ISO 8601 string to a datetime object
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 datetime format: {value}")

    @classmethod
    def serialize_datetime(cls, value: datetime, info: SerializationInfo) -> str:
        if isinstance(value, datetime):
            # Convert datetime object back to an ISO 8601 string
            return value.isoformat()
        raise ValueError("Expected a datetime object for serialization")
