from pathlib import Path, PosixPath
from typing import Any, List, Optional, TypeVar
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from mongomv.utils import not_none_return
from datetime import datetime

from .enums import Collections


PymongoService = TypeVar("PymongoService")


class MetaEntity(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    service: Optional[PymongoService] = Field(default=None, exclude=True, repr=False)
    collection: Optional[Collections] = Field(default=None, exclude=True, repr=False)

    id: Optional[ObjectId] = Field(default_factory=lambda: ObjectId(), frozen=True, alias="_id")
    name: str
    tags: list[str] = Field(default_factory=list)
    date: datetime = Field(default_factory=datetime.now, frozen=True)


    @not_none_return
    def add_tag(self, tags: list[str]) -> Optional[str]:
        for el in tags:
            if not isinstance(el, str):
                raise TypeError(f"Tags must be `list[str]`, not `list[{type(el)}]`")
        
        result = self.service.update(
            instance=self.collection.name,
            obj_id=self.id,
            update="$addToSet",
            value={"tags": {"$each": tags}}
        )
        if result == 1:
            self.tags = list(set(self.tags) | set(tags))
            return f"Model successfully updated, added tags: {tags}"


    @not_none_return
    def remove_tag(self, tags: list[str]) -> Optional[str]:
        for el in tags:
            if not isinstance(el, str):
                raise TypeError(f"Tags must be `list[str]`, not `list[{type(el)}]`")
        result = self.service.update(
            instance=self.collection.name,
            obj_id=self.id,
            update="$pull",
            value={"tags": {"$in": tags}}
        )
        if result == 1:
            self.tags = list(set(self.tags) - set(tags))
            return f"Model successfully updated, removed tags: {tags}"        


    @not_none_return
    def rename(self, new_name: str) -> Optional[str]:
        result = self.service.update(
            instance=self.collection.name,
            obj_id=self.id,
            update="$set",
            value={"name": new_name}
        )
        if result == 1:
            self.name = new_name
            return f"Model successfully updated, new name: {new_name}"


    def delete(self) -> bool:
        return self.service.delete(instance=self.collection.name, obj_id=self.id)
        

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True, by_alias=True)


class ModelParams(BaseModel):
    parameter: str = Field(frozen=True)
    value: Any


class ModelMetrics(BaseModel):
    metric: str = Field(frozen=True)
    value: Any


class SerializedModelEntity(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ObjectId = Field(default_factory=lambda: ObjectId(), frozen=True, alias="_id")
    entity_id: ObjectId
    serialized_model_path: str
    filename: str
    chunkSize: int = Field(default=261120, frozen=True)
    length: Optional[int] = None
    uploadDate: datetime = Field(default_factory=datetime.now, frozen=True)


class ModelEntity(MetaEntity):
    collection: Collections = Field(default=Collections.models, exclude=True, repr=False)

    params: Optional[List[ModelParams]] = Field(default_factory=list)
    metrics: Optional[List[ModelMetrics]] = Field(default_factory=list)
    description: Optional[str] = None
    experiment_id: Optional[ObjectId] = None
    serialized_model: Optional[SerializedModelEntity] = None


    @not_none_return
    def _set_experiment_id(self, experiment_id: ObjectId | None) -> Optional[bool]:
        result = self.service.update(
            instance="models",
            obj_id=self.id,
            update="$set",
            value={"experiment_id": experiment_id}
        )
        if result == 1:
            self.experiment_id = experiment_id
            return True


    @not_none_return
    def add_param(self, params: ModelParams) -> Optional[str]:
        assert type(params) == ModelParams, "params must be `ModelParams` type"

        result = self.service.update(
            instance="models",
            obj_id=self.id,
            update="$push",
            value={"params": params.model_dump()}
        )
        if result == 1:
            self.params.append(params)
            return f"Params successfully added"


    @not_none_return
    def remove_param(self, param_name: str) -> Optional[str]:
        index = None
        for el in self.params:
            if el.parameter == param_name:
                index = self.params.index(el)
        if index is None:
            raise KeyError(f"There is no parameter with {param_name} name.")
        
        result = self.service.update(
            instance="models",
            obj_id=self.id,
            update="$pull",
            value={"params": {"parameter": {"$in": [param_name]}}}
        )
        if result == 1:
            self.params.pop(index)
            return "Params successfully removed"


    @not_none_return
    def add_metric(self, metrics: ModelMetrics):
        assert type(metrics) == ModelMetrics, "metrics must be `ModelMetrics` type"

        result = self.service.update(
            instance="models",
            obj_id=self.id,
            update="$push",
            value={"metrics": metrics.model_dump()}
        )
        if result == 1:
            self.metrics.append(metrics)
            return f"Metrics successfully added"


    @not_none_return
    def remove_metric(self, metric_name: str):
        index = None
        for el in self.metrics:
            if el.metric == metric_name:
                index = self.metrics.index(el)
        if index is None:
            raise KeyError(f"There is no parameter with {metric_name} name.")
        
        result = self.service.update(
            instance="models",
            obj_id=self.id,
            update="$pull",
            value={"metrics": {"metric": {"$in": [metric_name]}}}
        )
        if result == 1:
            self.metrics.pop(index)
            return "Metrics successfully removed"


    @not_none_return
    def set_description(self, description: str):
        result = self.service.update(
            instance="models",
            obj_id=self.id,
            update="$set",
            value={"description": description}
        )
        if result == 1:
            self.description = description
            return "Description set"


    @not_none_return
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
        model_path: Path = Path(model_path) if isinstance(model_path, str) else model_path

        assert type(model_path) == PosixPath, "File path must be `pathlib.Path` or `str` type"
        assert model_path.exists(), "File does not exist"
        assert self.serialized_model is None, "There is serialized model, please delete this one"

        self.serialized_model = SerializedModelEntity(
            entity_id=self.id,
            serialized_model_path=model_path.as_posix(),
            filename=filename
        )
        with self.service.uow as uow:
            if uow.gridfs.put(model_path, self.serialized_model.model_dump(by_alias=True)):
                return "Model successfully serialized"


    @not_none_return
    def load_model(self, model_path: Optional[Path | str] = None):
        """Load model from MongoDB file storage using GridFS.
        
        Requires serialized model id (look `dump_model`)
        and model. If model path not set, then default path is `cwd/tmp/filename`.
        """
        if self.serialized_model is None:
            raise KeyError("There is no serialized model") 
        with self.service.uow as uow:
            if uow.gridfs.get(self.serialized_model.id, model_path):
                self.serialized_model.serialized_model_path = model_path
                return "Model successfully loaded"


    @not_none_return
    def delete_model(self) -> Optional[str]:
        assert type(self.serialized_model) == SerializedModelEntity

        with self.service.uow as uow:
            if uow.gridfs.delete(obj_id=self.serialized_model.id):
                self.serialized_model = None
                return "Serialized model successfully deleted from MongoDB file storage"


    def summary(self):
        print(f"Model name:................ {self.name}")
        print(f"Model tags:................ {self.tags}")
        print(f"Model description:......... {self.description}")
        print(f"Model creation date: ...... {self.date}")


class ExperimentEntity(MetaEntity):
    collection: Collections = Field(default=Collections.experiments, exclude=True, repr=False)

    models: Optional[List[ObjectId]] = Field(default_factory=list)


    @not_none_return
    def add_model(self, model: ModelEntity):
        assert isinstance(model, ModelEntity)
        assert model.experiment_id is None, f"Model is already linked to {model.experiment_id}"
        assert model.service is not None, "There is no service in model"

        result = self.service.update(
            instance="experiments",
            obj_id=self.id,
            update="$addToSet",
            value={"models": {"$each": [model.id]}}
        )
        if result == 1:
            self.models.append(model.id)
            if model._set_experiment_id(experiment_id=self.id):
                model.experiment_id = self.id
                return f"Model {model.name} successfully added to experiment"


    @not_none_return
    def remove_model(self, model: ModelEntity):
        assert isinstance(model, ModelEntity)
        assert model.id in self.models, "Model not in models"
        assert model.experiment_id == self.id, "Model does not linked to experiment"
        assert model.service is not None, "There is not service in model"

        result = self.service.update(
            instance="experiments",
            obj_id=self.id,
            update="$pull",
            value={"models": {"$in": [model.id]}}
        )
        if result == 1:
            if model._set_experiment_id(experiment_id=None):
                index = self.models.index(model.id)
                self.models.pop(index)
                return f"Model {model.name} successfully removed from experiment"
