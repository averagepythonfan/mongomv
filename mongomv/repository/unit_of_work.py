from typing import Type

from pymongo import MongoClient

from .repo import ExperimentsRepository, ModelsRepository, GridFSRepository


class UnitOfWork:

    experiments: Type[ExperimentsRepository]
    models: Type[ModelsRepository]

    def __init__(self, mongo_client: MongoClient):
        self.client = mongo_client

    def __enter__(self):
        self.session = self.client.start_session()

        self.experiments = ExperimentsRepository(session=self.session)
        self.models = ModelsRepository(session=self.session)
        self.gridfs = GridFSRepository(session=self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            raise exc_val
        else:
            self.session.end_session()
