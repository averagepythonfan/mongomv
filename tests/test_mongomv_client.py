import pytest
from mongomv import MongoMVClient
from mongomv.schemas import ExperimentEntity
from tests.conftest import TEST_MONGO_URI


@pytest.fixture(scope="module")
def mongomv_client():
    cl = MongoMVClient(mongo_uri=TEST_MONGO_URI)
    yield cl


@pytest.mark.usefixtures("mongomv_client")
class TestMongoMVClient:

    def test_create_experiment(self, mongomv_client: MongoMVClient):
        exp = mongomv_client.create_experiment(name="test1", tags=["testing"])
        assert isinstance(exp, ExperimentEntity)
