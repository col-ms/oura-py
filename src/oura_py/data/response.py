from dataclasses import dataclass


@dataclass
class Result:
    """The core response envelope returned by the HTTP request manager."""

    status_code: int
    message: str
    data: dict

    def __post_init__(self) -> None:
        expected_types = {
            "status_code": int,
            "message": str,
            "data": dict,
        }
        for name, expected_type in expected_types.items():
            value = getattr(self, name)
            if not isinstance(value, expected_type):
                raise TypeError(f"{name} must be {expected_type}, got {type(value)}")
