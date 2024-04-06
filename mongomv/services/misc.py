import datetime
from typing import Union, List, Any
from mongomv.schemas import FindBy, UpdateExperiment, UpdateModel, UpdateModelBase



def query(find_by: FindBy, value: Union[str, datetime.datetime, List[str]]):
    if find_by is FindBy.name:
        return {"name": value }
    elif find_by is FindBy.tags:
        return {"tags": {"$in": value}}
    elif find_by is FindBy.date:
        return {"date": {"$lt": datetime.datetime.fromisoformat(value)}}
    elif find_by is FindBy.id:
        return {"_id": value }


def update_query(
        update: Union[UpdateExperiment, UpdateModel, UpdateModelBase],
        value: Any
):
    if update is UpdateExperiment.rename:
        return {"$set": {"name": value}}
    elif update is UpdateExperiment.add_tag:
        return {"$push": {"tags": value}}
    elif update is UpdateExperiment.remove_tag:
        return {"$pull": {"tags": value}}
    elif update is UpdateExperiment.add_model:
        return {"$push": {"models": value}}
    elif update is UpdateExperiment.remove_model:
        return {"$pull": {"models": value}}

    elif update is UpdateModelBase.rename:
        return {"$set": {"name": value}}
    elif update is UpdateModelBase.add_tag:
        return {"$push": {"tags": value}}
    elif update is UpdateModelBase.remove_tag:
        return {"$pull": {"tags": value}}
    elif update is UpdateModelBase.set_description:
        return {"$set": {"description": value}}

    elif update is UpdateModel.add_params:
        return {"$push": {"params": value}}
    elif update is UpdateModel.remove_params:
        return {"$pull": {"params": {"parameter": {"$in": [value]}}}}
    elif update is UpdateModel.add_metric:
        return {"$push": {"metrics": value}}
    elif update is UpdateModel.remove_metric:
        return {"$pull": {"metrics": {"metric": {"$in": [value]}}}}
    elif update is UpdateModel.set_config:
        return {"$set": {"config": value}}
    elif update is UpdateModel.set_weights:
        return {"$set": {"weights": value}}
