from __future__ import annotations
import random
from typing import Callable

class Manager:
    pass

class Subject:
    def output(self):
        pass

    def _validate_num(self, lower_bound, upper_bound, action: Callable, value, property_name) -> None:
        if type(value) in (int, float):
            if lower_bound <= value <= upper_bound:
                action()
            else:
                raise ValueError(f"Monitor {property_name} must be between {lower_bound} and {upper_bound} inclusive.")
        else:
            raise TypeError(f"Monitor {property_name} must be a numerical value, but {value} of type {type(value)} was given.")


class IDObjectManager(Manager):
    """
    This class represents the general behavior of various other managers, like a VariableManager, ListManager,
    etc., whose items are stored as key-value pairs in a dictionary rather than as a list.
    The keys are always these unique IDs consisting of a variety of character spam, with the contents depending
    on the type of object generated. The fact, however, is that all of these managers fundamentally work in the same
    way, so this part of the class can be "factored out" of all of them, allowing them all to inherit from it here.
    """

    def __init__(self, id_dict, subtype: type[IDObject] | Callable) -> None:
        self._items = [subtype(key, id_dict[key]) for key in id_dict]

    @staticmethod
    def generate_id(l=20):
        valid_characters = "!#$%()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        id = "".join([random.choice(valid_characters) for i in range(l)])
        return id

    def output(self):
        # With this, subtypes (e.g. variables, lists, etc.) will only need to "output" their values;
        # the "key" part of the output is handled by the manager.
        return {
            i._id: i.output() for i in self._items
        }

class SearchableByName(IDObjectManager):
    def by_name(self, name):
        """
        Get all values that correspond to a given `name`.
        """
        return [i for i in self._items if i.name == i]

class HasXY(Subject):
    @property
    def x(self) -> float:
        """
        The x-coordinate of this subject.
        """
        return self._x
    
    @x.setter
    def x(self, value):
        self._validate_num(
            -240, 240,
            lambda: setattr(self, "_x", value),
            value,
            "x-coordinate"
        )

    @property
    def y(self) -> float:
        """
        The y-coordinate of this subject.
        """
        return self._y

    @y.setter
    def y(self, value):
            self._validate_num(
            -180, 180,
            lambda: setattr(self, "_y", value),
            value,
            "y-coordinate"
        )

class HasWidthHeight(Subject):
    @property
    def width(self) -> float:
        """
        The width of this monitor in pixels.
        """
        return self._width
    
    @width.setter
    def width(self, value):
        if type(value) not in (int, float):
            raise TypeError(f"Width value must be a numerical type, but {value} of type {type(value)} was received.")
        
        if not (1 <= value <= 240):
            raise ValueError(f"Width value ({value}) must be within 1 and 240 inclusive.")

        self._width = value

    @property
    def height(self) -> float:
        """
        The height of this monitor in pixels.
        """
        return self._height
    
    @height.setter
    def height(self, value):
        if type(value) not in (int, float):
            raise TypeError(f"Height value must be a numerical type, but {value} of type {type(value)} was received.")
        
        if not (1 <= value <= 180):
            raise ValueError(f"Height value ({value}) must be within 1 and 240 inclusive.")

        self._height = value

class IDObject(Subject):
    def __init__(self, id) -> None:
        self._id = id
