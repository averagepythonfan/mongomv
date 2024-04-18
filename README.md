# MongoMV - fast, light and clear framework to versioning your machine learning models

## Why MongoMV?

1. It simple: only Pymongo and Pydantic dependecies
2. We develope machine learning models
3. We use MongoDB in production
4. We need light and fast framework to versioning models
5. We use MongoMV

## How it works:
![Scheme](docs/pics/scheme.jpg)

## Install now

* `pip install https://github.com/averagepythonfan/mongomv/archive/main.zip`

## Firstly, we need to up our MongoDB. Docker compose example:
```
# docker-compose.yml
version: "3.3"

services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: secret
    ports:
      - "27017:27017"
```

and then up mongodb container:
```
~$: docker compose up -d
```

## Model Serialization:
- [TensorFlow and Keras](https://www.tensorflow.org/guide/keras/serialization_and_saving)
- [XGBoost](https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html)
- [sk-learn](https://scikit-learn.org/stable/model_persistence.html)
- [LightGBM](https://lightgbm.readthedocs.io/en/latest/R/reference/lgb.save.html)
- [PyTorch](https://pytorch.org/tutorials/beginner/saving_loading_models.html)

## Code example:

```Python
>>> from mongoumv.client import MongoMVClient
>>> client = MongoMVClient("mongodb://root:secret@localhost:27017")
>>> exp = client.create_experiment(name="test_exp", tags=["test", "dev"])
>>> exp.id
... ObjectId('658432fe394f866bc0096605')
>>> md = client.create_model(name="test_md", tags=["test", "v0.1"])
>>> md.id
... ObjectId('6584339e394f866bc0096607')
>>> path = "your_serialized_model_path"
>>> md.dump_model(model_path=path, filename="your_model_filename")
... "Model successfully serialized"
>>> exp.add_model(md)
... "Model test_md successfully added to experiment"

```
