from kurt3.has_id import IDObject, SearchableByName

class ListManager(SearchableByName):
    def __init__(self, list_dict) -> None:
        super().__init__(list_dict, ScratchList)
        self.__lists = self._items # Alias for readability

    def create_list(self, name: str, value: list =[]) -> None:
        """
        Create a new list. Leaving the `value` field empty appends a new empty list.
        Will check for naming conflicts before creating and raise an error if the list already exists.
        """

        # Check for existence; this really needs to be moved to allow checking other targets as well.
        for l in self.__lists:
            if l.name == name:
                raise ValueError(f"List {name} already exists.")
        
        # Validate list contents before setting
        for item in value:
            if type(item) not in (int, float, str):
                raise ValueError(f"List values must be numerical or string-type values, but {item} of type {type(item)} was received.")

        self.__lists.append(ScratchList(
            ListManager.generate_id(), 
                [
                    name,
                    value
                ]
            )
        )
    
    def remove_variable(self, name):
        match = [v for v in self.__lists if v.name == name]
        if match:
            self.__lists.remove(match[0])
        else:
            raise Warning(f"Could not delete variable {name}: variable does not exist.")

class ScratchList(IDObject):
    def __init__(self, id, values) -> None:
        super().__init__(id)
        self.__name = values[0]
        self.__value = values[1]
    
    @property
    def name(self) -> str:
        """
        The name of the list.
        """

        return self.__name
    
    @property
    def value(self) -> list:
        """
        The contents of the list, represented as a Python list.
        """
        return self.__value

    @value.setter
    def value(self, new_value):
        if type(new_value) is list:
            for item in new_value:
                if type(item) not in (int, float, str):
                    raise ValueError(f"List values must be numerical or string-type values, but {item} of type {type(item)} was received.")
            
            self.__value = self.value

        else:
            raise TypeError(f"List must be a list of numeric or string-type values, but {new_value} of type {type(new_value)} was received.")

    def output(self):
        return [self.__name, self.__value]