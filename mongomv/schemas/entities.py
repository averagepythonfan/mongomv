from mongomv.core import Entity

from .models import Experiments, Models



class ModelEntity(Models, Entity):

    def add_param(self):
        pass

    def remove_param(self):
        pass

    def add_metric(self):
        pass

    def remove_metric(self):
        pass

    def set_description(self):
        pass

    def dump_model(self):
        pass

    def load_model(self, path: str):
        pass


class ExperimentEntity(Experiments, Entity):

    def add_model(self):
        pass

    def add_tag(self):
        print("its `add_tag`")
    
    def remove_tag(self):
        print("its `remove_tag`")
    
    def rename(self):
        print("its `rename`")
    
    def delete(self):
        print("its `delete`")

    def remove_model(self):
        pass

    def summary(self):
        pass