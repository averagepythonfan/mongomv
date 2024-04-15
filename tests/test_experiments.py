"""Testing ExperimentEntity properties."""

import pytest
from mongomv import MongoMVClient
from mongomv.schemas import ExperimentEntity, ModelEntity
from tests.conftest import TEST_MONGO_URI


@pytest.fixture(scope="module")
def experiment():
    client = MongoMVClient(uri=TEST_MONGO_URI)
    exp = client.create_experiment(name="fixture", tags=["testing", "pytest"])
    yield exp
    exp.delete()


@pytest.fixture(scope="module")
def model():
    client = MongoMVClient(uri=TEST_MONGO_URI)
    md = client.create_model(name="test_model", tags=["testing", "pytest"])
    yield md
    md.delete()


# @pytest.mark.usefixtures("mongomv_client")
class TestExperimentEntity:

    
    def test_add_model_to_experiment(self, experiment: ExperimentEntity, model: ModelEntity):
        response = experiment.add_model(model=model)
        assert type(response) == str
        assert model.experiment_id == experiment.id
        assert model.id in experiment.models


    def test_remove_model_from_experiment(self, experiment: ExperimentEntity, model: ModelEntity):
        response = experiment.remove_model(model=model)
        assert type(response) == str
        assert model.id not in experiment.models
        assert model.experiment_id == None
