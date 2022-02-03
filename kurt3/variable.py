import random

from kurt3.has_id import IDObject, SearchableByName

class VariableManager(SearchableByName):
    # The thing about these variables is that they're listed in a dict, where the key is an arbitrary, unique
    # identifier for each variable. This makes them not very convenient for an object-oriented representation.
    # Hence, we convert them into a list for internal usage.
    def __init__(self, variable_dict) -> None:
        super().__init__(variable_dict, Variable)
        # self.__variables = self.__items # Alias for code readability

        # self.__variables = [Variable(k, variable_dict[k]) for k in variable_dict]
    
    def by_name(self, name):
        return [v for v in self.__variables if v.name == name]

    def create_variable(self, name, value):
        for var in self.__variables:
            if var.name == name:
                raise ValueError(f"Variable {name} already exists.")
        
        self.__variables.append(Variable(
                VariableManager.generate_id(), 
                [name, value]
            )
        )
    
    def remove_variable(self, name):
        match = [v for v in self.__variables if v.name == name]
        if match:
            self.__variables.remove(match[0])
        else:
            raise Warning(f"Could not delete variable {name}: variable does not exist.")

class Variable(IDObject):
    def __init__(self, id, values: list) -> None:
        super().__init__(id)
        self.__name = values[0]
        self.__value = values[1]
    
    @property
    def name(self):
        return self.__name
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if type(new_value) in (int, float, str):
            self.__value = self.value
        else:
            raise TypeError(f"Variable must have a numeric or string-type value, but {new_value} of type {type(new_value)} was received.")

    def output(self) -> list:
        return [self.__name, self.__value]