
class TemplateNotFoundException(Exception):
    def __init__(self,template_name:str):
        self._template_name=template_name

    def __str__(self):
        return f"There is no template with name {self._template_name}"


class TemplateAlreadyExistsException(Exception):
    def __init__(self,template_name:str):
        self._template_name=template_name

    def __str__(self):
        return f"There is already template with name {self._template_name}"

class ParsingErrorException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return f"Oops there is prsing error"

if __name__ == "__main__":
    pass
