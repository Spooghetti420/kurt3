from __future__ import annotations
from kurt3.comment import Comment
from kurt3.subject import IDObject, IDObjectManager


class BlockManager(IDObjectManager):
    def __init__(self, block_dict) -> None:
        super().__init__(BlockManager.create_block, block_dict)

    def add_block(self, block: Block):
        self._items.append(block)

    @staticmethod
    def create_block(id, block_dict):
        # Avoid using keyword as argument
        block_dict["_next"] = block_dict["next"]
        del block_dict["next"]

        if block_dict["topLevel"] is True:
            return TopLevelBlock(id, **block_dict)
        else:
            return Block(id, **block_dict)

class Block(IDObject):
    def __init__(self,
        id = None,
        opcode = None,
        _next = None,
        parent = None,
        inputs = {},
        fields = {},
        shadow = False,
        topLevel = True,
        comment = None
    ) -> None:
        super().__init__(id)
        self.__opcode = opcode
        self._next = _next
        self._parent = parent
        self.__inputs = InputManager(inputs)
        self.__fields = FieldsManager(fields)
        self.__shadow = shadow
        self.__top_level = topLevel
        if comment:
            self.__comment = comment
    
    @property
    def opcode(self) -> str:
        """
        The internal opcode that represents the block, e.g. `event_broadcast`.
        """
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
    def inputs(self) -> InputManager:
        """
        Return the inputs to this block.
        """
        return self.__inputs
    
    @property
    def fields(self) -> dict:
        """
        Return the fields applicable to this block.
        """
        return self.__fields
    
    @property
    def has_shadow(self):
        """
        Whether the block has a shadow behind it in the editor.
        """
        return self.__shadow
    
    @has_shadow.setter
    def set_shadow(self, value):
        if type(value) is bool:
            self.__shadow = value
        else:
            raise TypeError(f"Shadow must be a boolean value, but {value} of type {type(value)} was received.")
    
    @property
    def is_top_level(self) -> bool:
        """
        Whether the variable is a top-level block (True) or attached below another block (False).
        """
        return self.__top_level
    
    def set_next(self, next) -> None:
        """
        Replace this block's "next" block with another, deleting any blocks attached to it previously.
        """
        if self._next is not None:
            if type(next) is Block:
                next.remove_next()
                self._next = next.__id
            elif type(next) is str:
                # maybe check that this variable exists
                # also need to remove "next" values from block
                self._next = next
        else:
            raise KeyError("Error setting block's child block: block already has a next block.")

    def remove_next(self) -> None:
        if type(self._next) is not None:
            self.next.remove_next()
            self.next = None

    def output(self) -> dict:
        default = {
            "opcode": self.__opcode,
            "next": self._next,
            "parent": self._parent,
            "inputs": self.__inputs.output(),
            "fields": self.__fields.output(),
            "shadow": self.__shadow,
            "topLevel": self.__top_level,
        }
        try:
            out = default | {"comment": self.__comment}
            return out
        except AttributeError:
            return default

class TopLevelBlock(Block):
    def __init__(self,
        id = None,
        x = 0,
        y = 0,
        **kwargs
    ) -> None:
        super().__init__(id, **kwargs)
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self._validate_num(
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
        self._validate_num(
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
    def __init__(self, input_dict: dict) -> None:
        super().__init__(BlockInput, input_dict)

class BlockInput(IDObject):
    def __init__(self, id, value) -> None:
        super().__init__(id)
        self.__value = value
    
    # Idk what else to add here
    def output(self):
        return self.__value

class FieldsManager(IDObjectManager):
    def __init__(self, input_dict) -> None:
        super().__init__(BlockFields, input_dict)

class BlockFields(IDObject):
    def __init__(self, id, value) -> None:
        super().__init__(id)
        self.__value = value
    
    def output(self):
        return self.__value
