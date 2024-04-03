from typing import Any, Optional, List
from pymongo import MongoClient
from gridfs import GridFS


class MongoMVClient:

    serialized_models_db = "serialized"
    mv_db = "mongomv"
    experiments_collection = "experiments"
    models_collections = "models"


    def __init__(self, mongo_uri: str, **kwargs: Any) -> None:
        """Enter the mongo URI, also accept `MongoClient` args"""
        self.client = MongoClient(mongo_uri, kwargs, timeoutMS=100)
        
        assert len(self.client.list_databases()) != 0
        
        self.serialized_db = self.client.get_database(name=self.serialized_models_db)
        self.fs = GridFS(self.serialized_db)
    

    def create_experiment(self, name: str, tags: list):
        pass

    def create_model(self,
                     name: str,
                     tags: List[str],
                     params: Optional[List[dict]] = None,
                     description: str = ""):
        pass


    def list_of_experiments(self):
        pass


    def list_of_models(self, experiment_id: str):
        pass



    def find_experiment_by(self):
        pass

    def find_model_by(self):
        pass
