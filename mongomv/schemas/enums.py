from enum import Enum


class Collections(Enum):
    experiments = "experiments"
    models = "models"


class Instance(Enum):
    experiment = "experiment"
    model = "model"


class FindBy(Enum):
    id = "id"
    name = "name"
    date = "date"
    tags = "tags"


class UpdateExperiment(Enum):
    rename = "rename"
    add_tag = "add_tag"
    remove_tag = "remove_tag"
    add_model = "add_model"
    remove_model = "remove_model"


class UpdateModelBase(Enum):
    rename = "rename"
    add_tag = "add_tag"
    remove_tag = "remove_tag"
    set_description = "set_description"


class UpdateModel(Enum):
    add_params = "add_params"
    remove_params = "remove_params"
    add_metric = "add_metric"
    remove_metric = "remove_metric"
    set_config = "set_config"
    set_weights = "set_weights"
