from __future__ import annotations
from kurt3.subject import IDObject, Searchable

class VariableManager(Searchable):
    def __init__(self, variable_dict) -> None:
        super().__init__(Variable, variable_dict)
    
    def create_variable(self, name: str, value: int | float | str) -> None:
        """
        Add a variable with a given `name` and `value` to the target.
        Will check for naming conflicts before creating and raise an error if the variable already exists.
        """

        # Ensure name is a string before proceeding
        name = str(name)

        # Check the stage's variables for global variables also
        for var in self.__variables:
            if var.name == name:
                raise ValueError(f"Variable {name} already exists.")
        
        if type(value) not in (int, float, str):
            raise TypeError(f"Error creating variable {name}: variable value must be numerical or string-typed, but {value} of type {type(value)} was received.")

        self.__variables.append(Variable(
                VariableManager.generate_id(), 
                [name, value]
            )
        )
    
    def remove_variable(self, name):
        """
        Removes a variable from a target. Raises a warning if the variable does not exist.
        """
        match = [v for v in self.__variables if v.name == name]
        if match:
            self.__variables.remove(match[0])
        else:
            raise Warning(f"Could not delete variable {name}: variable does not exist.")

class Variable(IDObject):
    def __init__(self, id_, values: list) -> None:
        super().__init__(id_)
        self.__name = values[0]
        self.__value = values[1]
    
    @property
    def name(self) -> str:
        """
        The name of the variable.
        """
        return self.__name
    
    @property
    def value(self) -> int | float | str:
        """
        The value of the variable. Either a number or a string.
        """

        return self.__value
        

    @value.setter
    def value(self, new_value) -> None:
        """Set the value of the variable. Value must be numerical or string."""
        
        if type(new_value) in (int, float, str):
            self.__value = self.value
        else:
            raise TypeError(f"Variable must have a numeric or string-type value, but {new_value} of type {type(new_value)} was received.")

    def output(self) -> list:
        return [self.__name, self.__value]