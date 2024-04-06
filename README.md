# MongoMV - fast, light and clear framework to versioning your TensorFlow models

## What is that all about?

1. We develope machine learning models
2. We use MongoDB in production
2. We need light and fast framework to versioning models
3. We use MongoMV

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

## Code example:

```Python
>>> from mongoumv.client import MongoMVClient
>>> client = CorfuClient("mongodb://test:test@localhost:27017")
>>> exp = client.create_experiment(name="test_del", tags=["test", "delete"])
>>> exp.id
... ObjectId('658432fe394f866bc0096605')
>>> md = client.create_model(name="test_md", tags=["test", "model"])
>>> md.id
... ObjectId('6584339e394f866bc0096607')

```
