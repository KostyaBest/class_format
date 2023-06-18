import unittest
#Own
import main


class FileTemplteSaverTest(unittest.TestCase):
    def test_get_template_not_found_exception(self):
        with self.assertRaises(main.TemplateNotFoundException):
            saver = main.FileTemplateSaver()
            saver.get("second")
    def test_asset_equal_template_readlines(self):
        saver=main.FileTemplateSaver()
        self.assertEqual("{Person{\"name\":\"string\",\"last_name\":\"string\"}}\n",saver.get("first"))

    def test_saving_template(self):
        template="{Person{\"name\":\"string\",\"last_name\":\"string\"}}"
        saver=main.FileTemplateSaver()
        saver.save(template)
        with open(f"{saver._path}/Person","r") as f:
            template_from_file_list=f.readlines()
        template_from_file=""
        for line in template_from_file_list:
            template_from_file+=line
        template+="\n"
        self.assertEqual(template,template_from_file)

class ClassFormatParsingTest(unittest.TestCase):
    def test_parsing_template(self):
        pass
    def test__split_templates_and_fields(self):
        template="{Person{\"name\":\"string\",\"last_name\":\"string\"}}"
        must_be={"name":"string","last_name":"string"}
        result=main._split_templates_and_fields(template)
        self.assertEqual(must_be,result) 
    def test_parsing_array(self):
        pass

class ClassFormatSerializingTest(unittest.TestCase):
    def test_serializing_template(self):
        pass
    def test_serializing_array(self):
        pass

if __name__ == "__main__":
    unittest.main()
    
