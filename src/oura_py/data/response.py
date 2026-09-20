from dataclasses import dataclass
from typing import Any


@dataclass
class Result:
    """Minimal response envelope returned by the HTTP request manager."""

    status_code: int
    data: Any


class OuraResponse[T]:
    def __init__(
        self,
        data: Any,
        model_type: type[T] | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        self._data = data
        self._model_type = model_type
        self._metadata = metadata or {}

        self._model_cache: T | list[T] | None = None

    def raw(self) -> Any:
        return self._data

    def model(self) -> T | list[T]:
        if self._model_type is None:
            raise TypeError("No data model defined for this response")

        if self._model_cache is not None:
            return self._model_cache

        if isinstance(self._data, list):
            self._model_cache = [
                self._model_type.model_validate(item) for item in self._data
            ]
        else:
            self._model_cache = self._model_type.model_validate(self._data)

        return self._model_cache

    def to_polars(self):
        raise NotImplementedError("Polars conversion planned for a future release")

    def to_pandas(self):
        raise NotImplementedError("Pandas conversion planned for a future release")

    @property
    def metadata(self) -> dict[str, Any]:
        return self._metadata
