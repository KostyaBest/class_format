


"""
1){Person{"name":"string","last_name":"string"}}

2)Person:[{"name1","last_name1"},{"name2","last_name2"}]

"""

#from abc import ABC,abstractmethod
from os.path import isfile
from collections import namedtuple
from dataclasses import dataclass

#OWN
from exceptions import TemplateNotFoundException,TemplateAlreadyExistsException,ParsingErrorException
from interfaces import ITemplateSaver,ITemplate


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

@dataclass
class Saver:
    template_saver:ITemplateSaver
    def get_template(self,template_name:str):
        template_saver.get(template_name)
    def save_template(self,template_name:str)->None:
        template_saver.save(template_name)
    def get_array(self,array:str)->list[list]:
        return

def parse(data:str)->object:
    wrong_start_signs=[";","}",":","'","\"","(",")",]
    if data[0] == '{':
        return get_class_template(data)
    for c in wrong_start_signs:
        if data[0] == c:
            raise ParsingErrorException()
    return _get_obect_list(data) 

def get_class_template(data:object)->str:
    brakets_count=0
    data=_parse_whitespaces(data)
    is_first=True
    new_data={}
    for i in range(len(data)):
        if data[i] =='{' and is_first:
           pass 
        if brakets_count == 0:
            if data[i] == '{':
                brakets_count+=1
                continue
        if brakets_count == 1:
            if data[i] == '}':
                brakets_count-=1
                continue
    return data

def serialize_template(data:object)->str:
    string="{"
    is_first_field=True
    string+=type(data).__name__+"{"
    fields=data.__dict__
    for (field_name,field_type) in fields.items():
        if is_first_field:
            string+=f"{field_name}:{type(field_type)}"
            is_first_field=False
            continue
        string+=f",{field_name}:{type(field_type)}"

    string+="}}"
    return string

def serialize_data(template_name:str,data_list:list[object])->str:
    serialized_data=f"{template_name}:"+"["
    is_first_object=True
    is_first_in_obj_str=True
    for obj in data_list:
        if is_first_object:
            obj_str="{"
            is_first_object=False
        else:
            obj_str=",{"
            is_first_in_obj_str=True
        for (field_name,field_value) in obj.__dict__.items():
            if is_first_in_obj_str:
                obj_str+=f"{field_value}"
                is_first_in_obj_str=False
                continue
            obj_str+=f",{field_value}"
        obj_str+="}"
        serialized_data+=obj_str

    serialized_data+="]"
    return serialized_data

def _get_obect_list(data:str)->list[object]:
    brackets_count=0
    first_bracket_index=0
    class_name=""
    for i in range(len(data)):
        if data[i] == '[':
            first_bracket_index=i
            break
        else:
            class_name+=data[i]
    return class_name



def _parse_whitespaces(data:str)->str:
    quotation_mark_count=0
    string=""
    for i in range(len(data)):
        if quotation_mark_count == 0:
            if data[i] == '"':
                quotation_mark_count+=1
                string+=data[i]
                continue
            if data[i] == ' ':
                continue
            string+=data[i]
        if quotation_mark_count == 1:
            if data[i] == '"':
                quotation_mark_count=0
                string+=data[i]
                continue
            string+=data[i]
    return string


"""
1){Person{"name":"string","last_name":"string"}}

2)Person:[{"name1","last_name1"},{"name2","last_name2"}]

1){PersonWithAge{Person{"name":"string","last_name":"string"},"age":"int"}

2)PersonWithAge:[{{"name1","last_name1"},12},{{"name2","last_name2"},32}]
"""
#{"name":"string","last_name":"string"}
def _split_templates_and_fields(template:str)->dict:
    quotation_mark_counter=0
    template_dictionary={}
    is_key=True
    key_word=""
    value_word=""
    brackets_counter=0
    for i in range(len(template)):
        if template[i] == "{":
            brackets_counter +=1
            continue
        if template[i] == "}":
            brackets_counter -=1
            continue
        if is_key:
            if template[i] == '"' and quotation_mark_counter == 0:
                quotation_mark_counter+=1
                continue
            if template[i] == '"' and quotation_mark_counter == 1:
                quotation_mark_counter-=1
                is_key=False
                continue
            if template[i]==":":
                continue
            if quotation_mark_counter == 0:
                continue
            else:
                key_word+=template[i]
        else:
            if template[i] == '"' and quotation_mark_counter == 0:
                quotation_mark_counter+=1
                continue
            if template[i] == '"' and quotation_mark_counter == 1:
                quotation_mark_counter-=1
                template_dictionary[key_word]=value_word
                key_word=""
                value_word=""
                is_key=True
                continue
            if template[i]==":":
                continue
            if quotation_mark_counter == 0:
                continue
            else:
                value_word+=template[i]
                continue
    return template_dictionary

def _get_list_of_fields_from_object_string_buffer(object_string_buffer:str)->list[str]:
    quotation_mark_counter=0
    list_of_fields=[]
    word=""
    for i in range(len(object_string_buffer)):
        if object_string_buffer[i] == '"' and quotation_mark_counter==0:
            quotation_mark_counter+=1
            continue
        if object_string_buffer[i] == '"' and quotation_mark_counter==1:
            quotation_mark_counter-=1
            list_of_fields.append(word)
            word=""
            continue
        if object_string_buffer[i] == "{":
            continue
        if object_string_buffer[i] == "," and quotation_mark_counter<1:
            continue
        else:
            word+=object_string_buffer[i]
    return list_of_fields


def _match_object_with_template(template_name:str,template:dict,obj_list:list)->object:
    object_class=namedtuple(template_name,[t for t in template.keys()])
    #TODO here must be type checking
    #for field_name,field_type in template_name.items():

    new_object_tuple=tuple(obj_list)
    new_object=object_class(*new_object_tuple)
    return new_object

def _split_array_and_fields(array:str)->list[list]:
    #quotation_mark_counter for "
    quotation_mark_counter=0
    # braces_counter for { and}
    braces_counter=0
    #brackets_counter for [
    brackets_counter=0
    objects=[]
    was_first_bracket=False
    object_string_buffer=""
    for i in range(len(array)):
        if was_first_bracket:
            if brackets_counter>0:
                if array[i] =="{":
                    braces_counter+=1
                    continue
                if array[i] == "}":
                    list_of_fields=_get_list_of_fields_from_object_string_buffer(object_string_buffer)
                    objects.append(list_of_fields)
                    object_string_buffer=""
                    braces_counter-=1
                    continue
                if array[i] == ",":
                    continue
                if array[i] == "[":
                    brackets_counter+=1
                    continue
                if array[i] == "]":
                    brackets_counter-=1
                    continue
                else:
                    object_string_buffer+=array[i]
            if array[i] =="{":
                braces_counter+=1
                continue
            if array[i] == "}":
                list_of_fields=_get_list_of_fields_from_object_string_buffer(object_string_buffer)
                objects.append(list_of_fields)
                object_string_buffer=""
                braces_counter-=1
                continue
            #continue
        if array[i]=="[":
            was_first_bracket=True
            brackets_counter+=1
    return objects

def _get_class_name_from_array(array:str)->str:
    word=""
    for i in range(len(array)):
        if array[i] == "[":
            break
        word+=array[i]
    return word

#For Refactoring maybe there is way to implement via generators
def _try_to_match_arrays_with_template(template:str,array:str)->list[object]:
    try:
        template_dict=_split_templates_and_fields(template)
        list_of_object_fields=_split_array_and_fields(array)
        array_of_objects=[]
        template_name=_get_class_name_from_array(array)
        print(list_of_object_fields)
        for obj in list_of_object_fields:
            #print(obj)
            array_of_objects.append(_match_object_with_template(template_name,template_dict,obj))
        return array_of_objects
    except Exception as e:
        raise e.message


if __name__ == "__main__":
    pass
