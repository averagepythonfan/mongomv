from typing import Any, Dict, Literal, Optional

from bson import ObjectId
from pymongo import MongoClient

from mongomv.repository import UnitOfWork
from mongomv.utils import not_none_return

Instance = Literal["experiments", "models"]


class PymongoCRUDService:

    def __init__(self, mongo_uri: str, **kwargs):
        self.uow = UnitOfWork(MongoClient(mongo_uri, **kwargs))


    @not_none_return
    def create(self, instance: Instance, data: Dict) -> bool:
        if instance == "experiments":
            with self.uow:
                return self.uow.experiments.save_one(data)
        elif instance == "models":
            with self.uow:
                return self.uow.models.save_one(data)
        else:
            raise ValueError("Instance must be `experiments` or `models`")


    @not_none_return
    def read(self,
             instance: Instance,
             find_by: Dict,
             is_list: bool = False) -> Optional[Dict]:
        if instance == "experiments":
            if is_list:
                with self.uow:
                    return list(self.uow.experiments.get_many(get_by=find_by))
            else:
                with self.uow:
                    return self.uow.experiments.get_one(get_by=find_by)
        elif instance == "models":
            if is_list:
                with self.uow:
                    return list(self.uow.models.get_many(get_by=find_by))
            else:
                with self.uow:
                    return self.uow.models.get_one(get_by=find_by)
        else:
            raise ValueError("Instance must be `experiments` or `models`")


    @not_none_return
    def update(self,
               instance: Instance,
               obj_id: ObjectId,
               update: Literal["$set", "$push", "$pull", "$addToSet"],
               value: Any) -> Optional[int]:

        if update not in ["$set", "$push", "$pull", "$addToSet"]:
            raise ValueError(f"Update must be `$set`, `$addToSet`, `$push` or `$pull`, not {update}")

        if instance == "experiments":
            with self.uow:
                return self.uow.experiments.update_by_object_id(obj_id=obj_id, update_query={update: value})
        elif instance == "models":
            with self.uow:
                return self.uow.models.update_by_object_id(obj_id=obj_id, update_query={update: value})
        else:
            raise ValueError("Instance must be `experiments` or `models`")


    @not_none_return
    def delete(self, instance: Instance, obj_id: ObjectId) -> Optional[int]:
        if instance == "experiments":
            with self.uow:
                return self.uow.experiments.delete(obj_id=obj_id)
        elif instance == "models":
            with self.uow:
                return self.uow.models.delete(obj_id=obj_id)
        else:
            raise ValueError("Instance must be `experiments` or `models`")
