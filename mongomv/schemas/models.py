from typing import Any, List, Optional, Union
from attrs import define, field, setters, Factory, validators
from bson import ObjectId

from mongomv.core import MetaEntity


class ExperimentEntity(MetaEntity):
    models: Optional[List[ObjectId]] = field(default=Factory(list))
    @models.validator
    def check(self, attribute, value):
        for el in value:
            if not isinstance(el, ObjectId):
                raise ValueError()

    def add_model(self, obj_id):
        if not isinstance(obj_id, ObjectId):
            raise TypeError("Model must be `ObjectId` type, not {t}".format(t=type(obj_id)))

    def remove_model(self, obj_id):
        pass


@define
class ModelParams:
    parameter: str = field(kw_only=True, validator=validators.instance_of(str))
    value: Any = field(kw_only=True)

@define
class ModelMetrics:
    metric: str = field(kw_only=True, validator=validators.instance_of(str))
    value: Union[int, float, str] = field(kw_only=True)


class ModelEntity(MetaEntity):
    params: Optional[List[ModelParams]] = field(default=Factory(list))
    @params.validator
    def check(self, attribute, value):
        for el in value:
            if not isinstance(el, ModelParams):
                raise ValueError("Model params must be `ModelParams` type, not {t}".format(t=type(value)))
    metrics: Optional[List[ModelMetrics]] = field(default=Factory(list))
    @metrics.validator
    def check(self, attribute, value):
        for el in value:
            if not isinstance(el, ModelMetrics):
                raise ValueError("Model params must be `ModelMetrics` type, not {t}".format(t=type(value)))
    description: Optional[str] = field(default=Factory(''))
    serialized_model_id: Optional[ObjectId] = field(on_setattr=setters.frozen, validator=validators.instance_of(ObjectId))

    def dump_model(self, model):
        pass

    def load_model(self):
        pass