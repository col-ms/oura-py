from dataclasses import dataclass
from typing import Any

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


class OuraResponse[T]:
    def __init__(
        self,
        data: Any,
        model_type: type[T] | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        self._data = data
        self._model_type = model_type
        self._metadata = metadata

        self._model_cache: T | list[T] | None = None
        self._polars_cache: None = None

    def raw(self) -> Any:
        return self._data

    def model(self) -> T | list[T]:
        if self._model_type is None:
            raise TypeError("No data model defined for this response")

        if self._model_cache:
            return self._model_cache

        if isinstance(self._data, list):
            self._model_cache = [
                self._model_type.model_validate(item) for item in self._data
            ]
        else:
            self._model_cache = self._model_type.model_validate(self._data)

        return self._model_cache

    def to_polars(self):
        raise NotImplementedError("Polars conversion yet to be implemented")

    def to_pandas(self):
        raise NotImplementedError("Pandas conversion yet to be implemented")

    @property
    def metadata(self) -> dict[str, Any]:
        return self._metadata
