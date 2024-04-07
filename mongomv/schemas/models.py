from typing import Any, List, Optional, TypeVar
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


    def delete(self) -> bool:
        return self.service.delete(instance=self)
        

    def to_dict(self):
        return self.model_dump(exclude_none=True, by_alias=True)


class ExperimentEntity(MetaEntity):
    collection: Collections = Field(default=Collections.experiments, exclude=True, repr=False)

    models: Optional[List[ObjectId]] = Field(default_factory=list)

    def add_model(self, model: ObjectId):
        assert isinstance(model, ObjectId)
        
        result = self.service.update(
            instance=self,
            update=UpdateExperiment.add_model,
            value=model
        )
        self.models.append(model)
        return result


    def remove_model(self, model: ObjectId):
        assert isinstance(model, ObjectId)
        result = self.service.update(
            instance=self,
            update=UpdateExperiment.remove_model,
            value=model
        )
        index = self.models.index(model)
        self.models.pop(index)
        return result


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

        result=  self.service.update(
            instance=self,
            update=UpdateModel.add_params,
            value=params
        )
        self.params.append(params)
        return result


    def remove_param(self, params: ModelParams):
        result = self.service.update(
            instance=self,
            update=UpdateModel.remove_params,
            value=params
        )
        index = self.params.index(params)
        self.params.pop(index)
        return result


    def add_metric(self, metrics: ModelMetrics):
        assert type(metrics) == ModelParams, "metrics must be `ModelMetrics` type"
        result = self.service.update(
            instance=self,
            update=UpdateModel.add_metric,
            value=metrics
        )
        self.metrics.append(metrics)
        return result


    def remove_metric(self, metrics: ModelMetrics):
        result = self.service.update(
            instance=self,
            update=UpdateModel.remove_metric,
            value=metrics
        )
        ind = self.metrics.index(metrics)
        self.metrics.pop(ind)
        return result


    def set_description(self, description: str):
        result = self.service.update(
            instance=self,
            update=UpdateModelBase.set_description,
            value=description
        )
        self.description = description
        return result


    def dump_model(self, model_path, filename) -> str:
        """Dump model to MongoDB file storage using GridFS.
        
        Requires serialized model path and filename.
        Return `str`: "Model successfully serialized"

        :param:
            - model_path: might be `Path` or `str` type
            - filename: str

        Keras example:
        >>> filename = "cv_v01.keras"
        >>> path = f"/tmp/{filename}"
        >>> model.save(path)
        >>> from mongomv import MongoMVClient
        >>> client = MongoMVClient(mongo_uri)
        >>> md = client.create_model(name="keras", tags=["dev", "testing"])
        >>> md.dump_model(model_path=path, filename=filename)
        ... "Model successfully serialized"
        """
        self.serialized_model = self.service.dump(model_path, filename)
        return "Model successfully serialized"


    def load_model(self, model_path: str = None):
        """Load model from MongoDB file storage using GridFS.
        
        Requires serialized model id (look `dump_model`)
        and model. If model path not set, then default path is `cwd/tmp/filename`.
        """
        if self.serialized_model is None:
            raise KeyError("There is no serialized model")

        if self.service.load(self.serialized_model, model_path):
            return "Model successfully loaded"


    def summary(self):
        print(f"Model name:................ {self.name}")
        print(f"Model tags:................ {self.tags}")
        print(f"Model description:......... {self.description}")
        print(f"Model creation date: ...... {self.date}")
