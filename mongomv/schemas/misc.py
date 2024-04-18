from typing import Annotated

from bson.objectid import ObjectId as _ObjectId
from pydantic.functional_validators import AfterValidator


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")
    return value


ObjectId = Annotated[str, AfterValidator(check_object_id)]


def object_id_as_str():
    return _ObjectId().binary.hex()
