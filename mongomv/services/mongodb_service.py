import os
from pathlib import Path
from types import NoneType
from typing import Optional, Union, List
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient, CursorType
from pymongo.results import UpdateResult
from gridfs import GridFS

from mongomv.schemas import (
    ModelEntity,
    ExperimentEntity,
    FindBy,
    UpdateExperiment,
    UpdateModel,
    ModelParams,
    ModelMetrics,
    Collections
)

from .misc import query, update_query


Instance = Union[ModelEntity, ExperimentEntity]


class PymongoService:
    """PyMongo CRUD service.
    
    Requires a mongodb uri."""

    serialized_models_db_name = "serialized"
    mongomv_db_name = "mongomv"
    experiments_collection_name = "experiments"
    models_collections_name = "models"

    def __init__(self, uri: Union[str, bytes] = None, timeoutMS: int = 100) -> None:
        self.client = MongoClient(uri, timeoutMS=timeoutMS)
        self.mongomv = self.client.get_database(name=self.mongomv_db_name)
        self.serialized_models = self.client.get_database(name=self.serialized_models_db_name)
        self.fs = GridFS(database=self.serialized_models, collection="models")

        self.experiments = self.mongomv.get_collection(name=self.experiments_collection_name)
        self.models = self.mongomv.get_collection(name=self.models_collections_name)


    def dump(self, model_path: Path | str, filename: str) -> ObjectId:
        """Dumps model to MongoDB with GridFS.
        
        Return `ObjectId` of file.
        """
        model_path = Path(model_path) if isinstance(model_path, str) else model_path
        if model_path.exists():
            with open(file=model_path, mode="rb") as md:
                if md.readable():
                    data = md.read()
                    return self.fs.put(data=data, filename=filename)
                else:
                    raise TypeError("File not readable")
        else:
            raise FileNotFoundError("File does not exists")


    def load(self, model_object_id: ObjectId, model_path: str | Path = None) -> bool:
        cur = self.fs.find_one({"_id": model_object_id})
        assert type(cur) not in (None, NoneType), "Serialized model not found"

        if model_path:
            model_path = Path(model_path) if isinstance(model_path, str) else model_path
        else:
            model_path = Path(os.getcwd()).joinpath(f"/tmp/{cur.filename}")
        if model_path.exists():
            raise FileExistsError("File exists")

        with open(model_path, "wb") as md:
            md.write(cur.read())
        return True


    @staticmethod
    def _validate_cursor(cur: CursorType, is_list: bool = False) -> Union[list, str]:
        """Validation function for `read` pymongo crud service method"""
        listed = list(cur)

        if len(listed) == 0:
            raise KeyError("There is no matched data")
        else:
            if is_list:
                return listed
            else:
                if len(listed) == 1:
                    return listed
                else:
                    raise ValueError("There is multiple data, but flag `is_list` = False")


    def create(self, instance: Instance) -> None:
        """Create an instance of model or experiment."""
        if isinstance(instance, ModelEntity):
            self.models.insert_one(instance.to_dict())
        elif isinstance(instance, ExperimentEntity):
            self.experiments.insert_one(instance.to_dict())
        else:
            raise KeyError("Instance must be `ModelEntity` or `ExperimentEnitity`")


    def read(self,
             collection: Collections,
             find_by: FindBy,
             value: Union[str, datetime, List[str]] = None,
             is_list: bool = False) -> List[Union[ExperimentEntity, ModelEntity]]:
        params = {
            "find_by": find_by,
            "value": value
        }
        q = query(**params)

        if collection is Collections.experiments:
            cur = self.experiments.find(filter=q)
            validated: list | str = self._validate_cursor(cur=cur, is_list=is_list)
            return [ExperimentEntity(**el) for el in validated]
        elif collection is Collections.models:
            cur = self.models.find(filter=q)
            validated: list | str = self._validate_cursor(cur=cur, is_list=is_list)
            return [ModelEntity(**el) for el in validated]
        else:
            raise ValueError(
                "Instance must be enum's `Collections`, not {t}".format(t=type(collection))
            )
    

    def update(self,
               instance: Instance,
               update: Union[UpdateExperiment, UpdateModel],
               value: Union[str, ModelParams, ModelMetrics, ObjectId]) -> Optional[str]:
        if isinstance(instance, ExperimentEntity):
            if update is UpdateExperiment.add_model:
                cur = self.models.find(filter={"_id": value})
                if len(list(cur)) == 0:
                    raise KeyError(f"Model not found, ID: {value}. Add model to database.")
            q = update_query(update=update, value=value)
            result: UpdateResult = self.experiments.update_one(
                filter={"_id": instance.id},
                update=q
            )
            if result.modified_count != 0:
                return "Experiment successfully updated"
            else:
                raise KeyError(f"Experiment update failed, id: {instance.id}")
        elif isinstance(instance, ModelEntity):
            q = update_query(update=update, value=value)
            result: UpdateResult = self.models.update_one(
                filter={"_id": instance.id},
                update=q
            )
            if result.modified_count != 0:
                return "Model successfully updated"
            else:
                raise KeyError(f"Model update failed, id: {instance.id}")
        else:
            raise ValueError(
                "Instance must be `ExperimentEntity` or `ModelEntity`, not {t}".format(t=type(instance))
            )


    def delete(self, instance: Instance) -> Optional[bool]:
        f = {"_id": instance.id}
        if isinstance(instance, ExperimentEntity):
            result = self.experiments.delete_one(filter=f)
            if result.deleted_count == 1:
                return True
            else:
                raise KeyError(f"experiment did not deleted, id: {instance.id}")
        elif isinstance(instance, ModelEntity):
            result = self.models.delete_one(filter=f)
            # delete serialized model
            if result.deleted_count == 1:
                return True
            else:
                raise KeyError(f"model did not deleted, id: {instance.id}")
