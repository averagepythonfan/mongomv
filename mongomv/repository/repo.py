from typing import Dict, Any

from pymongo.client_session import ClientSession
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult
from bson import ObjectId


class PymongoRepository:

    database_name: str = "mongomv"
    collection: str = None


    def __init__(self, session: ClientSession):
        self.session = session
        self.db = self.session.client.get_database(name=self.database_name)
        self.collection = self.db.get_collection(name=self.collection)


    def save_one(self, data: Dict) -> bool:
        result: InsertOneResult = self.collection.insert_one(data, session=self.session)
        return result.acknowledged


    def get_many(self, get_by: Dict, projection: Dict = {}) -> Cursor:
        return self.collection.find(
            get_by,
            projection=projection,
            session=self.session
        )


    def get_one(self, get_by: Dict, projection: Dict = {}) -> Dict[Any, Any]:
        return self.collection.find_one(
            get_by,
            projection=projection,
            session=self.session
        )


    def update_by_object_id(self, obj_id: ObjectId, update_query: Dict) -> int:
        result: UpdateResult = self.collection.update_one(
            {"_id": obj_id},
            update=update_query,
            session=self.session
        )
        return result.modified_count


    def delete(self, obj_id: ObjectId) -> int:
        result: DeleteResult = self.collection.delete_one(
            {"_id": obj_id},
            session=self.session
        )
        return result.deleted_count


class ExperimentsRepository(PymongoRepository):
    collection = "experiments"


class ModelsRepository(PymongoRepository):
    collection = "models"
