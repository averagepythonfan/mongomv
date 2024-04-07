from bson import ObjectId
import pytest
from pydantic import ValidationError
from mongomv import MongoMVClient
from contextlib import nullcontext as does_not_raise
from mongomv.schemas import ExperimentEntity, ModelEntity, ModelParams


@pytest.mark.usefixtures("mongomv_client")
class TestMongoMVClient:


    @pytest.mark.parametrize(
        argnames="name, tags, expectation",
        argvalues=[
            ("first_try", ["v0.1.1", "alpha"], does_not_raise()),
            ("sec_try", ["v0.2.3", "beta", "temporary"], does_not_raise()),
            ("last_try", ["v0.5.2", "rc"], does_not_raise()),
            (12345, ["raise", "exception"], pytest.raises(ValidationError)),
            ("validation_error", [1, 45, 3], pytest.raises(ValidationError)),
        ]
    )
    def test_create_experiment(self, name, tags, expectation, mongomv_client: MongoMVClient):
        with expectation:
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
        argnames="name, tags, params, description, expectation",
        argvalues=[
            ("first_md", ["test1"], [ModelParams(parameter="seed", value=41)], "first model description", does_not_raise()),
            ("keras_md", ["test2"], [ModelParams(parameter="seed", value=42)], "keras model description", does_not_raise()),
            ("tf_md", ["test3"], [ModelParams(parameter="batch", value=50)], "tensorflow model description", does_not_raise()),
            (12234, ["test2"], [ModelParams(parameter="seed", value=42)], "keras model description", pytest.raises(ValidationError)),
            ("val_error", [23, 4, 2], [ModelParams(parameter="seed", value=42)], "keras model description", pytest.raises(ValidationError)),
            ("val_error", ["test6"], [ModelParams(parameter="seed", value=43)], 2345, pytest.raises(ValidationError)),
        ]
    )
    def test_create_model(self, name, tags, params, description, expectation, mongomv_client: MongoMVClient):
        with expectation:
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
