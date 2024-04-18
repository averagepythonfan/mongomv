from pathlib import Path
from typing import Any, Dict, Optional

from bson import ObjectId
from gridfs import GridIn, GridOut
from pymongo.client_session import ClientSession
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult


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



class GridFSRepository:

    database = "serialized"
    collection = "models"

    def __init__(self, session: ClientSession):
        self.session = session
        self.db = self.session.client.get_database(name=self.database)
        self.root_collection = self.db.get_collection(name=self.collection)
        self.gridin = GridIn
        self.gridout = GridOut


    def put(self, model_path: Path, data: Dict) -> Optional[bool]:
        with open(file=model_path, mode="rb") as file:
            if file.readable():
                with self.gridin(root_collection=self.root_collection, session=self.session, **data) as gridin:
                    if gridin.writeable():
                        if gridin.write(data=file.read()) is None:
                            return True
            else:
                raise FileExistsError("File not readable")


    def get(self, obj_id: ObjectId, model_path: Optional[Path] = None) -> Optional[bool]:
        with self.gridout(root_collection=self.root_collection, session=self.session, file_id=obj_id) as gridout:
            path: Path = model_path if model_path else gridout.serialized_model_path
            if path.exists():
                raise FileExistsError("File is already exists")
            if gridout.readable():
                with open(path, "wb") as md:
                    md.write(gridout.read())
                    return True


    def delete(self, obj_id: ObjectId):
        result = self.root_collection.files.delete_one({"_id": obj_id}, session=self.session)
        result_ = self.root_collection.chunks.delete_many({"files_id": obj_id}, session=self.session)
        if result.deleted_count != 0 and result_.deleted_count != 0:
            return True
