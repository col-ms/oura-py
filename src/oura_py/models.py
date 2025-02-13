from typing import Dict, List


class Result:
    """the result of an HTTP request operation.

    Attributes:
        status_code: An integer indicating the status code of the result.
        message: A human readable string describing the reason.
        data: A list of dictionaries (or single dictionary) containing the response data.
    """

    def __init__(self, status_code: int, message: str = "", data: List[Dict] = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class PersonalInfo:
    """The user's personal info.

    Attributes:
        id: The user's Oura API ID.
        age: The user's age.
        weight: The user's weight in kilograms.
        height: The user's height in meters.
        biological_sex: The user's biological sex.
        email: The user's email address.
    """

    def __init__(
        self,
        id: str,
        age: int,
        weight: float,
        height: float,
        biological_sex: str,
        email: str,
    ):
        self.id = str(id)
        self.age = int(age)
        self.weight = float(weight)
        self.height = float(height)
        self.sex = str(biological_sex)
        self.email = str(email)
