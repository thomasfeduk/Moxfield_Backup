from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from pydantic import StringConstraints
from pydantic_core import core_schema, CoreSchema

# Define your custom types using Annotated
StrPopulated = Annotated[str, StringConstraints(min_length=1, pattern=r'\S+')]
DateYmd = Annotated[str, StringConstraints(pattern=r'^\d{4}-\d{2}-\d{2}$')]


class DatetimeIso8601:
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: type, handler: Callable) -> CoreSchema:
        # Define a schema that checks the regex and then parses the datetime
        return core_schema.with_info_after_validator_function(
            cls.parse_datetime, core_schema.str_schema(pattern=r"^\d{4}(-\d{2}(-\d{2}(T\d{2}(:\d{2}(:\d{2}(\.\d{1,6})?)?)?(Z|[+-]\d{2}(:?\d{2})?)?)?)?)?$")
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