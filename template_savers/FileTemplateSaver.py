
"""
from path import path
from sys.path import append
"""
""" 
import path
import sys
 
# directory reach
directory = path.path(__file__).abspath()
 
# setting path
sys.path.append(directory.parent.parent)
 
# importing
from parentdirectory.interfaces import ITemplateSaver
""" 
from os.path import isfile
from os import path
#directory = path(__file__).abspath()
sys.path.append()
# using
#OWN
#from interfaces import ITemplateSaver

from ..interfaces import ITemplateSaver

class FileTemplateSaver(ITemplateSaver):
    def __init__(self):
        self._path="templates"
    def get(self,template_name:str):
        path=f"{self._path}/{template_name}"
        if isfile(path):
            with open(path,"r") as f:
                template_lines=f.readlines()
            lines=""
            for line in template_lines:
                lines+=line
            return lines
        raise TemplateNotFoundException(template_name)

    def save(self,template:str)->None:
        is_first=True
        template_name=""
        for i in range(len(template)):
            if template[i] =='{' and is_first:
                pass 
            if template[i]!='{':
                template_name+=template[i]
                continue
            if template[i] == '{' and not is_first:
                break
        path=f"{self._path}/{template_name}"
        if isfile(path):
            raise TemplateAlreadyExistsException(template_name)
        with open(path,"a") as f:
            f.writelines(template)


if __name__ == "__main__":
    pass
