from typing import Any, Literal, Optional, List, Union

# from mongomv.services import PymongoService
from mongomv.schemas import ModelEntity, ExperimentEntity, ModelParams, Collections, FindBy
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
        """Create an model instance.
        
        Requires name and tags. Optional params and description.
        Return `ModelEntity` (mongomv.schemas.ModelEntity) instance.
        Example:
        >>> md = client.create_model(name="keras_model", tags=["dev", "v0.1"])
        >>> md.id
        ... ObjectId('66105f81426f1640c3d7e167')
        """
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
        """Return list of `ExperimentEntity` instances.
        
        May set numbers and page.
        """
        cur = self.mongo_service.client.mongomv.experiments.find({})
        lst = [ExperimentEntity(**el, service=self.mongo_service) for el in cur]
        return lst[num*page:num*(page+1)]


    def list_of_models(self, num: int = 10, page: int = 0):
        """Return list of `ModelEntity` instances.
        
        May set numbers and page.
        """
        cur = self.mongo_service.client.mongomv.models.find({})
        lst = [ModelEntity(**el, service=self.mongo_service) for el in cur]
        return lst[num*page:num*(page+1)]


    def find_experiment_by(self,
                           find_by: Literal["id", "name", "date", "tags"],
                           value: str,
                           is_list: bool = False):
        """Find experiment by `id` or `name` or less than `date` or `tags`.

        May return list of experiments is `is_list` is `True`.
        """
        find_result = self.mongo_service.read(
            collection=Collections.experiments,
            find_by=FindBy(find_by),
            value=value,
            is_list=is_list
        )
        return find_result if is_list else find_result[0]


    def find_model_by(self,
                      find_by: Literal["id", "name", "date", "tags"],
                      value: str,
                      is_list: bool = False):
        """Find model by `id` or `name` or less than `date` or `tags`.

        May return list of experiments is `is_list` is `True`.
        """
        find_result = self.mongo_service.read(
            collection=Collections.models,
            find_by=FindBy(find_by),
            value=value,
            is_list=is_list
        )
        return find_result if is_list else find_result[0]
