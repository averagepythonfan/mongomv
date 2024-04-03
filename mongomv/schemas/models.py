from datetime import datetime
from typing import Any, AnyStr, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field

from .misc import ObjectId, object_id_as_str


JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


class MetaCollection(BaseModel):
    class Collection:
        name = None


class Experiments(MetaCollection):
    """Experiments base model.

    Uses as instance for any repository.
    For example:
    >>> class SyncExperimentRepository(PymongoRepository):
    ...     model = Experiments

    Requires set `class Collcection` and property `name`.
    Might be used in client section.
    """

    id: ObjectId = Field(default_factory=object_id_as_str, alias="_id")
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    date: datetime = datetime.now()
    models: Optional[List[ObjectId]] = []

    class Collection:
        name = "experiments"


class ModelParams(BaseModel):
    """Schema for Models."""
    parameter: Optional[str] = None
    value: Optional[Any] = None

class ModelMetrics(BaseModel):
    """Schema for Models."""
    metric: Optional[str] = None
    value: Optional[Union[int, float, str]] = None


class Models(MetaCollection):
    """`Models` base model.

    Uses as instance for any repository.
    For example:
    >>> class SyncExperimentRepository(PymongoRepository):
    ...     model = Models

    Requires set `class Collcection` and property `name`.
    Might be used in client section.
    """

    id: ObjectId = Field(default_factory=object_id_as_str, alias="_id")
    name: Optional[str] = None
    params: Optional[List[ModelParams]] = None
    tags: Optional[List[str]] = None
    metrics: Optional[List[ModelMetrics]] = None
    description: Optional[str] = None
    date: datetime = datetime.now()
    input_shape: Optional[Tuple[Any, Any]] = None
    config: Optional[JSONStructure] = None
    weights: Optional[JSONStructure] = None

    class Collection:
        name = "models"
