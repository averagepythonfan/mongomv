from attrs import define, field, setters, Factory, asdict, validators
from bson import ObjectId
from typing import List, Optional, Tuple, Union
from datetime import datetime


@define
class MetaEntity:

    # service: str = field(kw_only=True)
    
    _id: ObjectId = field(default=Factory(lambda: ObjectId()), on_setattr=setters.frozen)
    name: Optional[str] = field(kw_only=True)
    tags: Optional[List[str]] = field(default=Factory(list), kw_only=True)
    @tags.validator
    def check(self, attribute, value):
        for el in value:
            if not isinstance(el, str):
                raise ValueError() 
    date: datetime = field(default=Factory(datetime.now))

    @property
    def id(self):
        return self._id

    def add_tag(self, tags: list[str]):
        pass

    def remove_tag(self, tags: list[str]):
        pass

    def rename(self, new_name: str):
        pass

    def delete(self):
        pass

    def to_dict(self):
        return asdict(self)
