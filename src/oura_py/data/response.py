from dataclasses import dataclass

type JSONValue = (
    dict[str, JSONValue] | list[JSONValue] | str | int | float | bool | None
)


def _is_json_value(value: object) -> bool:
    if value is None or isinstance(value, (bool, int, float, str)):
        return True
    if isinstance(value, list):
        return all(_is_json_value(item) for item in value)
    if isinstance(value, dict):
        return all(
            isinstance(key, str) and _is_json_value(item) for key, item in value.items()
        )
    return False


@dataclass
class Result:
    """The core response envelope returned by the HTTP request manager."""

    status_code: int
    message: str
    data: JSONValue

    def __post_init__(self) -> None:
        if not isinstance(self.status_code, int):
            raise TypeError(f"status_code must be {int}, got {type(self.status_code)}")
        if not isinstance(self.message, str):
            raise TypeError(f"message must be {str}, got {type(self.message)}")
        if not _is_json_value(self.data):
            raise TypeError("data must be a JSON-compatible value")
