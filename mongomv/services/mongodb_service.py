from typing import Union
from pymongo import MongoClient

from mongomv.schemas import ModelEntity, ExperimentEntity


class PymongoService:

    serialized_models_db_name = "serialized"
    mongomv_db_name = "mongomv"
    experiments_collection_name = "experiments"
    models_collections_name = "models"

    def __init__(self, uri: Union[str, bytes] = None) -> None:
        self.client = MongoClient(uri, timeoutMS=100)
        self.mongomv = self.client.get_database(name=self.mongomv_db_name)
        self.serialized_models = self.client.get_database(name=self.serialized_models_db_name) 

        self.experiments = self.mongomv.get_collection(name=self.experiments_collection_name)
        self.models = self.mongomv.get_collection(name=self.models_collections_name)


    def create(self, instance: Union[ModelEntity, ExperimentEntity]):
        if isinstance(instance, ModelEntity):
            inserted = self.models.insert_one(instance.model_dump(exclude_none=True, by_alias=True))
        elif isinstance(instance, ExperimentEntity):
            inserted = self.experiments.insert_one(instance.model_dump(exclude_none=True, by_alias=True))
        else:
            raise KeyError("Instance must be `ModelEntity` or `ExperimentEnitity`")
        return inserted.inserted_id


    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass