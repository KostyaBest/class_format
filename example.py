


import main


data="{Person{\"name\"  :\"string\",  \"last_name\":\"string\"}   }"



#print(main.parse(data))
class Person:
    def __init__(self,name,last_name):
        self.name = name
        self.last_name=last_name

#print(main.serialize_template(Person("name2","last_name2")))
#print(main.serialize_data("Person",[Person("name2","last_name2"),Person("name3","last_name3")]))
array="Person[{\"name2\",\"last_name2\"},{\"name3\",\"last_name3\"},{\"last_name4\",\"last_name4\"}]"
#array2="Person[{\"name2\",\"last_name2\",\"3\"},{\"name3\",\"last_name3\",[\"name1\",\"last_name1\"]}]"
array2="Person[{\"name2\",\"last_name2\"},{\"name3\",\"last_name3\"]}]"

#print(main.parse(data))
parsed=main.parse(array)
print(parsed)


person_template="{Person{\"name\":\"string\",\"last_name\":\"string\"}}"

print(' ')
"""
print(main.get_class_template(data))
"""
print(' ')
"""
print(main._split_templates_and_fields(data))
"""

#print(main._split_array_and_fields(array))
#print(main._split_array_and_fields(array2))
#print(main._get_list_of_fields_from_object_string_buffer("{\"name\",\"last_name\"}"))


#print(main._match_object_with_template("Person",{"name":"string","last_name":"string"},["name1","last_name1"]))
#print(main._try_to_match_arrays_with_template(person_template,array2))
print(main._try_to_match_arrays_with_template(person_template,array))


