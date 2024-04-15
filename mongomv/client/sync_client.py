from datetime import datetime
from typing import Dict, Literal, Optional, List

from mongomv.services import PymongoCRUDService
from mongomv.utils import not_none_return
from mongomv.schemas import ModelEntity, ExperimentEntity, ModelParams


class MongoMVClient:
    """Mongo model versioning class.
    
    Require a mongodb URI string to initialize MongoClient.
    Also available several methods:
        - `create_experiment` -> ExperimentEntity
        - `create_model` -> ModelEntity
        - `list_of_experiments` -> List[ExperimentEntity]
        - `list_of_models` -> List[ModelEntity]
        - `find_experiment_by` -> List[ExperimentEntity] | ExperimentEntity
        - `find_model_by` -> List[ModelEntity] | ModelEntity.
    """

    serialized_models_db = "serialized"
    mv_db = "mongomv"
    experiments_collection = "experiments"
    models_collections = "models"


    def __init__(self, uri: str, **kwargs) -> None:
        """Enter the mongo URI, also accept `MongoClient` args.
        Initialize MongoDB client.
        Default arg for MongoClient: `timeoutMS` = 100.
        
        Example:
        >>> from mongomv import MongoMVCLient 
        >>> uri = "mongodb://root:secret@localhost:27017"
        >>> client = MongoMVCLient(uri)
        """
        self.crud = PymongoCRUDService(uri, **kwargs)
    

    @not_none_return
    def create_experiment(self, name: str, tags: list[str]):
        experiment = ExperimentEntity(
            service=self.crud,
            name=name,
            tags=tags
        )
        if self.crud.create(
            instance="experiments",
            data=experiment.model_dump(exclude_none=True, by_alias=True)
        ):
            return experiment


    @not_none_return
    def list_of_experiments(self, num: int = 10, page: int = 0):
        result = self.crud.read(instance="experiments", find_by={}, is_list=True)[num*page:num*(page+1)]
        return [ExperimentEntity(service=self.crud, **el) for el in result]


    @not_none_return
    def find_experiment_by(self,
                           find_by: Optional[Literal["id", "name", "date", "tags"]] = None,
                           value: Optional[str] = None,
                           query: Optional[Dict] = None,
                           is_list: bool = False):
        if find_by and query:
            raise ValueError("Only `find_by` and `value` or `query` must be specified, not both.")
        if find_by == "tags":
            value = {"$in": value}
        if find_by == "date":
            assert type(value) == datetime
            value = {"$lt": value}
        result = self.crud.read(
            instance="experiments",
            find_by={find_by: value},
            is_list=is_list
        )
        if is_list:
            return [ExperimentEntity(service=self.crud, **el) for el in result]
        else:
            return ExperimentEntity(service=self.crud, **result)


    @not_none_return
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
            service=self.crud,
            name=name,
            tags=tags,
            params=params,
            description=description
        )
        if self.crud.create(
            instance="models",
            data=model.model_dump(exclude_none=True, by_alias=True)
        ):
            return model


    @not_none_return
    def list_of_models(self, num: int = 10, page: int = 0):
        """Return list of `ModelEntity` instances.
        
        May set numbers and page.
        """
        result = self.crud.read(instance="models", find_by={}, is_list=True)[num*page:num*(page+1)]
        return [ModelEntity(service=self.crud, **el) for el in result]


    @not_none_return
    def find_model_by(self,
                      find_by: Optional[Literal["id", "name", "date", "tags"]],
                      value: Optional[str] = None,
                      query: Optional[dict] =None,
                      is_list: bool = False):
        """Find model by `id` or `name` or less than `date` or `tags`.

        May return list of experiments is `is_list` is `True`.
        """
        if find_by and query:
            raise ValueError("Only `find_by` and `value` or `query` must be specified, not both.")
        if find_by == "tags":
            value = {"$in": value}
        if find_by == "date":
            assert type(value) == datetime
            value = {"$lt": value}
        result = self.crud.read(
            instance="models",
            find_by={find_by: value},
            is_list=is_list
        )
        if is_list:
            return [ModelEntity(service=self.crud, **el) for el in result]
        else:
            return ModelEntity(service=self.crud, **result)
