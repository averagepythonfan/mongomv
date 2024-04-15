"""Testing MetaEntity properties:
    - `rename`
    - `add_tag`
    - `remove_tag`
    - `delete`."""

import pytest
from mongomv import MongoMVClient
from contextlib import nullcontext as does_not_raise
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


@pytest.mark.usefixtures("mongomv_client")
class TestMetaEntity:

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
    

    @pytest.mark.parametrize(
        argnames="new_name",
        argvalues=[
            ("keras_cv"),
            ("linear_reg"),
            ("Dev_LogReg"),
        ]
    )
    def test_rename_model(self, new_name, model: ModelEntity, mongomv_client: MongoMVClient):
        result = model.rename(new_name=new_name)
        assert type(result) == str
        md = mongomv_client.find_model_by(find_by="name", value=new_name)
        assert md.name == new_name


    @pytest.mark.parametrize(
        argnames="tags, expectation",
        argvalues=[
            (["new", "tags"], does_not_raise()),
            (["fail", 1], pytest.raises(TypeError)),
            (["valid", "tags"], does_not_raise()),
        ]
    )
    def test_add_tags_to_experiment(self, tags, expectation, experiment: ExperimentEntity, mongomv_client: MongoMVClient):
        with expectation:
            response = experiment.add_tag(tags=tags)
            assert type(response) == str
            exp = mongomv_client.find_experiment_by(find_by="tags", value=tags)
            for el in tags:
                assert el in exp.tags
    

    @pytest.mark.parametrize(
        argnames="tags, expectation",
        argvalues=[
            (["model", "tags"], does_not_raise()),
            (["error", 2], pytest.raises(TypeError)),
            (["several", "v0.1"], does_not_raise()),
        ]
    )
    def test_add_tags_to_model(self,  tags, expectation, model: ModelEntity, mongomv_client: MongoMVClient):
        with expectation:
            response = model.add_tag(tags=tags)
            assert type(response) == str
            md = mongomv_client.find_model_by(find_by="tags", value=tags)
            for el in tags:
                assert el in md.tags
