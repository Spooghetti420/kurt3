from __future__ import annotations
from operator import ne

from attr import has
from kurt3.has_id import IDObject, IDObjectManager


class BlockManager(IDObjectManager):
    def __init__(self, block_dict) -> None:
        super().__init__(block_dict, Block.create_block)

class Block(IDObject):
    def __init__(self, id, values) -> None:
        super().__init__(id)
        self.__opcode = values["opcode"]
        self.__next = values["next"]
        self.__parent = values["parent"]
        self.__inputs = InputManager(values["inputs"])
        self.__fields = values["fields"]
        self.__shadow = values["shadow"]
        self.__top_level = values["topLevel"]
        if "comment" in values:
            print("COMMENT EXISTS")
            self.__comment = values["comment"]

    @staticmethod
    def create_block(id, values):
        if values["topLevel"] is True:
            return TopLevelBlock(id, values)
        else:
            return Block(id, values)
    
    @property
    def opcode(self):
        return self.__opcode
    
    @property
    def next(self) -> Block | None:
        # Get the next block, as a Block object somehow
        pass
    
    @property
    def parent(self) -> Block | None:
        # Get parent block as a Block object
        pass

    @property
    def inputs(self):
        return self.__inputs
    
    @property
    def fields(self):
        return self.__fields
    
    @property
    def has_shadow(self):
        return self.__shadow
    
    @has_shadow.setter
    def set_shadow(self, value):
        if type(value) is bool:
            self.__shadow = value
    
    @property
    def is_top_level(self):
        return self.__top_level
    
    def set_next(self, next):
        if self.__next is not None:
            if type(next) is Block:
                self.__next = next.__id
            elif type(next) is str:
                # maybe check that this variable exists
                self.__next = next
        else:
            raise KeyError("Error setting block's child block: block already has a next block.")

    def remove_next(self):
        if type(self.__next) is not None:
            self.next.remove_next()
            self.next = None

    def output(self) -> dict:
        default = {
            "opcode": self.__opcode,
            "next": self.__next,
            "parent": self.__parent,
            "inputs": self.__inputs.output(),
            "fields": self.__fields,
            "shadow": self.__shadow,
            "topLevel": self.__top_level,
        }
        try:
            out = default | {"comment": self.__comment}
            print("output with comment")
            return out
        except AttributeError:
            return default

class TopLevelBlock(Block):
    def __init__(self, id, values) -> None:
        super().__init__(id, values)
        self.__x = values["x"]
        self.__y = values["y"]

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__validate_num(
            -2000,
            2000,
            lambda: setattr(self, "__x", value),
            value,
            "x-coordinate"
        )
    
    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__validate_num(
            -2000,
            2000,
            lambda: setattr(self, "__y", value),
            value,
            "y-coordinate"
        )
    
    def output(self) -> dict:
        return super().output() | {
            "x": self.__x,
            "y": self.__y
        }

class InputManager(IDObjectManager):
    def __init__(self, input_dict) -> None:
        super().__init__(input_dict, BlockInput)

class BlockInput(IDObject):
    def __init__(self, id, value) -> None:
        super().__init__(id)
        self.__value = value
    
    # Idk what else to add here
    def output(self):
        return self.__value
