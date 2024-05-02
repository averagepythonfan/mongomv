import pytest
from mongomv import MongoMVClient


TEST_MONGO_URI = "mongodb://test:test@localhost:27018"


@pytest.fixture(scope="session")
def mongomv_client():
    cl = MongoMVClient(uri=TEST_MONGO_URI)
    yield cl


@pytest.fixture(scope="module")
def model():
    client = MongoMVClient(uri=TEST_MONGO_URI)
    md = client.create_model(name="test_model", tags=["testing", "pytest"])
    yield md
    md.delete()
