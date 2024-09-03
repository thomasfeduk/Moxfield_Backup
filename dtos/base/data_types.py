from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from pydantic import StringConstraints
from pydantic_core import core_schema, CoreSchema
from pydantic_core.core_schema import SerializationInfo

# Define your custom types using Annotated
StrPopulated = Annotated[str, StringConstraints(min_length=1, pattern=r'\S+')]
DateYmd = Annotated[str, StringConstraints(pattern=r'^\d{4}-\d{2}-\d{2}$')]
DatetimeIso8601 = Annotated[str, StringConstraints(pattern=r"^\d{4}(-\d{2}(-\d{2}(T\d{2}(:\d{2}(:\d{2}(\.\d{1,6})?)?)?(Z|[+-]\d{2}(:?\d{2})?)?)?)?)?$")]
