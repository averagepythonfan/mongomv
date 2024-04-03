from abc import ABC, abstractmethod



class Entity(ABC):


    @abstractmethod
    def rename(self):
        raise NotImplementedError("`rename` method not implemented")


    @abstractmethod
    def add_tag(self):
        raise NotImplementedError("`add_tag` method not implemented")


    @abstractmethod
    def remove_tag(self):
        raise NotImplementedError("`remove` method not implemented")

    
    @abstractmethod
    def delete(self):
        raise NotImplementedError("`delete` method not implemented")
