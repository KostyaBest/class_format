
from abc import ABC,abstractmethod

class ITemplate(ABC):
    @abstractmethod
    def match(self,request:dict)->object:
        pass


class ITemplateSaver(ABC):
    @abstractmethod
    def get(self,template_name:str):
        pass
    @abstractmethod
    def save(self,template)->None:
        pass

if __name__ == "__main__":
    pass
