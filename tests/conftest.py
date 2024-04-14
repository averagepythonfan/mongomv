import pytest
from mongomv import MongoMVClient


TEST_MONGO_URI = "mongodb://test:test@localhost:27017"


@pytest.fixture(scope="session")
def mongomv_client():
    cl = MongoMVClient(uri=TEST_MONGO_URI)
    yield cl
