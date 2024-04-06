from typing import Any, Optional, List, Union

# from mongomv.services import PymongoService
from mongomv.schemas import ModelEntity, ExperimentEntity, ModelParams
from mongomv.services import PymongoService


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
        """Create an experiment instance.
        
        Requires name and tags. Return `ExperimentEntity` (mongomv.schemas.ExperimentEntity) instance.
        Example:
        >>> exp = client.create_experiment(name="keras_cv", tags=["dev", "v0.1"])
        >>> exp.id
        ... ObjectId('66105f81426f32b0c3d7e42f')
        """
        experiment = ExperimentEntity(name=name, tags=tags, service=self.mongo_service)
        self.mongo_service.create(instance=experiment)
        return experiment


    def create_model(self,
                     name: str,
                     tags: List[str],
                     params: Optional[List[ModelParams]] = [],
                     description: str = None) -> ModelEntity:
        model = ModelEntity(
            name=name,
            tags=tags,
            params=params,
            description=description,
            service=self.mongo_service
        )
        self.mongo_service.create(instance=model)
        return model


    def list_of_experiments(self, num: int = 10, page: int = 0):
        cur = self.mongo_service.client.mongomv.experiments.find({})
        return list(cur)[num*page:num*(page+1)]


    def list_of_models(self, num: int = 10, page: int = 0):
        cur = self.mongo_service.client.mongomv.models.find({})
        return list(cur)[num*page:num*(page+1)]


    def find_experiment_by(self):
        pass

    def find_model_by(self):
        pass
