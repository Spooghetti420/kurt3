from __future__ import annotations
import random
from typing import Callable

from kurt3.subject import Manager, Subject

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

class IDObject(Subject):
    def __init__(self, id) -> None:
        self._id = id
