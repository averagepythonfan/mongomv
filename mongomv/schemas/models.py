from typing import Any, List, Optional, Type, TypeVar, Union
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
# from mongomv.services import PymongoService
from datetime import datetime

from .enums import UpdateExperiment, UpdateModel, Collections, UpdateModelBase


PymongoService = TypeVar("PymongoService")


class MetaEntity(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    service: Optional[PymongoService] = Field(default=None, exclude=True, repr=False)
    collection: Optional[Collections] = Field(default=None, exclude=True, repr=False)

    id: Optional[ObjectId] = Field(default_factory=lambda: ObjectId(), frozen=True, alias="_id")
    name: str
    tags: list[str] = Field(default_factory=list)
    date: datetime = Field(default_factory=datetime.now, frozen=True)

    def add_tag(self, tags: list[str]):
        for el in tags:
            if not isinstance(el, str):
                raise TypeError(f"Tags must be `list[str]`, not `list[{type(el)}]`")
        self.tags.extend(tags)
        if self.collection is Collections.experiments:
            return self.service.update(
                instance=self,
                update=UpdateExperiment.add_tag,
                value=tags
            )
        elif self.collection is Collections.models:
            return self.service.update(
                instance=self,
                update=UpdateModelBase.add_tag,
                value=tags
            )


    def remove_tag(self, tags: list[str]):
        for el in tags:
            if not isinstance(el, str):
                raise TypeError(f"Tags must be `list[str]`, not `list[{type(el)}]`")
        self.tags = list(set(self.tags) - set(tags))
        if self.collection is Collections.experiments:
            return self.service.update(
                instance=self,
                update=UpdateExperiment.remove_tag,
                value=tags
            )
        elif self.collection is Collections.models:
            return self.service.update(
                instance=self,
                update=UpdateModelBase.remove_tag,
                value=tags
            )


    def rename(self, new_name: str):
        assert type(new_name) == str, f"new name must be `str`, not {type(new_name)}"
        self.name = new_name
        if self.collection is Collections.experiments:
            return self.service.update(
                instance=self,
                update=UpdateExperiment.rename,
                value=new_name
            )
        elif self.collection is Collections.models:
            return self.service.update(
                instance=self,
                update=UpdateModelBase.rename,
                value=new_name
            )


    def delete(self):
        return self.service.delete(instance=self)
        

    def to_dict(self):
        return self.model_dump(exclude_none=True, by_alias=True)


class ExperimentEntity(MetaEntity):
    collection: Collections = Field(default=Collections.experiments, exclude=True, repr=False)

    models: Optional[List[ObjectId]] = Field(default_factory=list)

    def add_model(self, model: ObjectId):
        return self.service.update(
            instance=self,
            update=UpdateExperiment.add_model,
            value=model
        )


    def remove_model(self, model: ObjectId):
        return self.service.update(
            instance=self,
            update=UpdateExperiment.remove_model,
            value=model
        )


class ModelParams(BaseModel):
    parameter: str = Field(frozen=True)
    value: Any

class ModelMetrics(BaseModel):
    metric: str = Field(frozen=True)
    value: Any


class ModelEntity(MetaEntity):
    collection: Collections = Field(default=Collections.models, exclude=True, repr=False)

    params: Optional[List[ModelParams]] = Field(default_factory=list)
    metrics: Optional[List[ModelMetrics]] = Field(default_factory=list)
    description: Optional[str] = None
    serialized_model: Optional[ObjectId] = None

    def add_param(self, params: ModelParams):
        assert type(params) == ModelParams, "params must be `ModelParams` type"
        return self.service.update(
            instance=self,
            update=UpdateModel.add_params,
            value=params
        )

    def remove_param(self, params: str):
        return self.service.update(
            instance=self,
            update=UpdateModel.remove_params,
            value=params
        )

    def add_metric(self, metrics: ModelMetrics):
        assert type(metrics) == ModelParams, "metrics must be `ModelMetrics` type"
        return self.service.update(
            instance=self,
            update=UpdateModel.add_metric,
            value=metrics
        )

    def remove_metric(self, metrics: ModelMetrics):
        return self.service.update(
            instance=self,
            update=UpdateModel.remove_metric,
            value=metrics
        )


    def set_description(self, description: str):
        return self.service.update(
            instance=self,
            update=UpdateModelBase.set_description,
            value=description
        )


    def dump_model(self):
        """GridFS"""
        pass

    def load_model(self, path: str):
        """GridFS"""
        pass

    def summary(self):
        print(f"Model name:................ {self.name}")
        print(f"Model tags:................ {self.tags}")
        print(f"Model description:......... {self.description}")
        print(f"Model creation date: ...... {self.date}")
