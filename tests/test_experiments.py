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


class TestExperimentEntity:

    @pytest.mark.parametrize(
        argnames="new_name",
        argvalues=[
            ("cv_1"),
            ("testing"),
            ("TestExperiment"),
        ]
    )
    def test_rename_experiment(self, new_name, experiment: ExperimentEntity):
        result = experiment.rename(new_name=new_name)
        assert type(result) == str
        