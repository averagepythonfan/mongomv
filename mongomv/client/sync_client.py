from typing import Any, Optional, List, Union

from bson import ObjectId


from mongomv.services import PymongoService
from mongomv.schemas import ModelEntity, ExperimentEntity


class MongoMVClient:

    serialized_models_db = "serialized"
    mv_db = "mongomv"
    experiments_collection = "experiments"
    models_collections = "models"


    def __init__(self, mongo_uri: str, **kwargs: Any) -> None:
        """Enter the mongo URI, also accept `MongoClient` args.
        Initialize MongoDB client.
        Default arg for MongoClient: `timeoutMS` = 100.
        
        Example:
        >>> from mongomv import MongoMVCLient 
        >>> uri = "mongodb://root:secret@localhost:27017"
        >>> client = MongoMVCLient(uri)
        """
        self.mongo_service = PymongoService(mongo_uri)
    

    def create_experiment(self, name: str, tags: list) -> ExperimentEntity:
        experiment = ExperimentEntity(name=name, tags=tags)
        self.mongo_service.create(instance=experiment)
        return experiment


    def create_model(self,
                     name: str,
                     tags: List[str],
                     params: Optional[List[dict]] = None,
                     description: str = "") -> ModelEntity:
        model = ModelEntity(
            name=name,
            tags=tags,
            params=params,
            description=description
        )
        self.mongo_service.create(instance=model)
        return model


    def list_of_experiments(self):
        pass


    def list_of_models(self, experiment_id: Union[str, ObjectId]):
        pass



    def find_experiment_by(self):
        pass

    def find_model_by(self):
        pass
