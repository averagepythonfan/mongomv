import pytest
from mongomv import MongoMVClient
from mongomv.schemas import ExperimentEntity, ModelEntity
from tests.conftest import TEST_MONGO_URI


@pytest.fixture(scope="module")
def experiment():
    client = MongoMVClient(mongo_uri=TEST_MONGO_URI)
    exp = client.create_experiment(name="fixture", tags=["testing", "pytest"])
    yield exp
    exp.delete()


@pytest.fixture(scope="module")
def model():
    client = MongoMVClient(mongo_uri=TEST_MONGO_URI)
    md = client.create_model(name="test_model", tags=["testing", "pytest"])
    yield md
    md.delete()


@pytest.mark.usefixtures("mongomv_client")
class TestExperimentEntity:

    @pytest.mark.parametrize(
        argnames="new_name",
        argvalues=[
            ("cv_1"),
            ("testing"),
            ("TestExperiment"),
        ]
    )
    def test_rename_experiment(self, new_name, experiment: ExperimentEntity, mongomv_client: MongoMVClient):
        result = experiment.rename(new_name=new_name)
        assert type(result) == str
        exp = mongomv_client.find_experiment_by(find_by="name", value=new_name)
        assert exp.name == new_name
