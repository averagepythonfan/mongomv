import pytest
from mongomv import MongoMVClient
from mongomv.schemas import ModelMetrics, ModelParams, ModelEntity
from tests.conftest import TEST_MONGO_URI



@pytest.fixture(scope="module")
def model():
    client = MongoMVClient(uri=TEST_MONGO_URI)
    md = client.create_model(name="test_model", tags=["testing", "pytest"])
    yield md
    md.delete()


class TestModelEntity:


    @pytest.mark.parametrize(
        argnames="params",
        argvalues=[
            (ModelParams(parameter="random_seed", value=42)),
            (ModelParams(parameter="batch", value=64)),
        ]
    )
    def test_add_params(self, params, model: ModelEntity):
        response = model.add_param(params=params)
        assert type(response) == str
        assert params in model.params
    

    @pytest.mark.parametrize(
        argnames="param_name",
        argvalues=[
            ("random_seed"),
            ("batch"),
        ]
    )
    def test_remove_params(self, param_name, model: ModelEntity):
        response = model.remove_param(param_name=param_name)
        assert type(response) == str
        assert param_name not in [el.parameter for el in model.params]


    @pytest.mark.parametrize(
        argnames="metrics",
        argvalues=[
            (ModelMetrics(metric="accuracy", value=0.7)),
            (ModelMetrics(metric="f1-score", value=0.64)),
        ]
    )
    def test_add_metric(self, metrics, model: ModelEntity):
        response = model.add_metric(metrics=metrics)
        assert type(response) == str
        assert metrics in model.metrics
    

    @pytest.mark.parametrize(
        argnames="metric_name",
        argvalues=[
            ("accuracy"),
            ("f1-score"),
        ]
    )
    def test_remove_metric(self, metric_name, model: ModelEntity):
        response = model.remove_metric(metric_name=metric_name)
        assert type(response) == str
        assert metric_name not in [el.metric for el in model.metrics]


    def test_set_description(self, model: ModelEntity):
        response = model.set_description(description="This is description of model")
        assert type(response) == str
