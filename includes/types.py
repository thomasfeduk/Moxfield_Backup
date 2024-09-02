from typing import Any, Dict, List

# Type alias for any valid JSON type. Primarily used for requests response.json()
JSONType = Dict[str, Any] | List[Any] | str | int | float | bool | None
