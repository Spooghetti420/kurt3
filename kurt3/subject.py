from typing import Callable


class Manager:
    pass

class Subject:
    def __validate_num(self, lower_bound, upper_bound, action: Callable, value, property_name) -> None:
        if type(value) in (int, float):
            if lower_bound <= value <= upper_bound:
                action()
            else:
                raise ValueError(f"Monitor {property_name} must be between {lower_bound} and {upper_bound} inclusive.")
        else:
            raise TypeError(f"Monitor {property_name} must be a numerical value, but {value} of type {type(value)} was given.")