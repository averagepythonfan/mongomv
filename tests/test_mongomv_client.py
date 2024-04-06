from bson import ObjectId
import pytest
from mongomv import MongoMVClient
from mongomv.schemas import ExperimentEntity, ModelEntity, ModelParams
from tests.conftest import TEST_MONGO_URI


@pytest.fixture(scope="module")
def mongomv_client():
    cl = MongoMVClient(mongo_uri=TEST_MONGO_URI)
    yield cl


@pytest.mark.usefixtures("mongomv_client")
class TestMongoMVClient:


    @pytest.mark.parametrize(
        argnames="name, tags",
        argvalues=[
            ("first_try", ["v0.1.1", "alpha"]),
            ("sec_try", ["v0.2.3", "beta", "temporary"]),
            ("last_try", ["v0.5.2", "rc"]),
        ]
    )
    def test_create_experiment(self, name, tags, mongomv_client: MongoMVClient):
        exp = mongomv_client.create_experiment(name=name, tags=tags)
        assert isinstance(exp, ExperimentEntity)
        assert exp.tags == tags
        assert exp.name == name


    @pytest.mark.parametrize(
            argnames="find_by, value",
            argvalues=[
                ("name", "sec_try"),
                ("tags", ["alpha"]),
            ]
    )
    def test_find_experiment_by(self, find_by, value, mongomv_client: MongoMVClient):
        exp = mongomv_client.find_experiment_by(find_by=find_by, value=value)
        assert type(exp.id) is ObjectId


    @pytest.mark.parametrize(
        argnames="name, tags, params, description",
        argvalues=[
            ("first_md", ["test1"], [ModelParams(parameter="seed", value=41)], "first model description"),
            ("keras_md", ["test2"], [ModelParams(parameter="seed", value=42)], "keras model description"),
            ("tf_md", ["test3"], [ModelParams(parameter="batch", value=50)], "tensorflow model description"),
        ]
    )
    def test_create_model(self, name, tags, params, description, mongomv_client: MongoMVClient):
        md = mongomv_client.create_model(
            name=name,
            tags=tags,
            params=params,
            description=description
        )
        assert isinstance(md, ModelEntity)
        assert md.name == name
        assert md.tags == tags
        assert md.params == params
        assert md.description == description


    @pytest.mark.parametrize(
            argnames="find_by, value",
            argvalues=[
                ("name", "keras_md"),
                ("tags", ["test3"]),
            ]
    )
    def test_find_model_by(self, find_by, value, mongomv_client: MongoMVClient):
        md = mongomv_client.find_model_by(find_by=find_by, value=value)
        assert type(md.id) is ObjectId


    def test_list_of_experiments(self, mongomv_client: MongoMVClient):
        lst = mongomv_client.list_of_experiments()
        assert len(lst) == 3
        for el in lst:
            assert el.delete()

    def test_list_of_models(self, mongomv_client: MongoMVClient):
        lst = mongomv_client.list_of_models()
        assert len(lst) == 3
        for el in lst:
            assert el.delete()
