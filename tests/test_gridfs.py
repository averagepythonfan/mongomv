import os
from pathlib import Path
from mongomv.schemas import ModelEntity
import pytest


@pytest.mark.usefixtures("model")
class TestGridFS:

    def test_dump_model(self, model: ModelEntity):
        path = Path(os.getcwd()).joinpath("text.txt")
        with open(path, "w") as file:
            file.write("This is test case for GridFS")
        result = model.dump_model(model_path=path, filename="text.txt")
        assert type(result) == str
        assert model.serialized_model is not None
        os.remove(path=path)


    def test_load_model(self, model: ModelEntity):
        path = Path(os.getcwd()).joinpath("text.txt")
        result = model.load_model(model_path=path)
        assert type(result) == str
        assert path.exists()
        os.remove(path=path)


    def test_delete_serialized_model(self, model: ModelEntity):
        result = model.delete_model()
        assert type(result) == str
