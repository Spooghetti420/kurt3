from __future__ import annotations
from re import S
from typing import Callable

from kurt3.subject import Subject

class MonitorManager:
    def __init__(self, monitor_list) -> None:
        self.__monitors = [Monitor.create_monitor(m) for m in monitor_list]
    
    # Make "__monitors" a readonly property
    @property
    def monitors(self):
        return self.__monitors

    def output(self) -> list[Monitor]:
        return [m.output() for m in self.__monitors]

class Monitor(Subject):
    """ Class that represents
        A base Monitor object is able to fully represent a Scratch list monitor, but note that
        a variable monitor requires a VariableMonitor object as it has three additional properties
        to encode.
    """
    def __init__(self, monitor_data) -> None:
        self.__id = monitor_data["id"] # Variable ID that the monitor is displaying
        self.__mode = monitor_data["mode"] # "list", "default", etc., specifies what kind of monitor this is
        self.__opcode = monitor_data["opcode"] # Either equal to "data_variable" or "data_listcontents"
        self.__params = monitor_data["params"]
        self.__sprite_name = monitor_data["spriteName"] # null, or string if the monitor is local to a sprite
        self.__value = monitor_data["value"]
        self.__width = monitor_data["width"]
        self.__height = monitor_data["height"]
        self.__x = monitor_data["x"]
        self.__y = monitor_data["y"]
        self.__visible = monitor_data["visible"]

    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def mode(self) -> str:
        return self.__mode
    
    @property
    def opcode(self) -> str:
        return self.__opcode
    
    @property
    def params(self):
        return self.__params
    
    @property
    def sprite_name(self) -> str:
        return self.__sprite_name
    
    @property
    def value(self) -> int | float | str:
        return self.__value
    
    @property
    def width(self) -> float:
        return self.__width
    
    @width.setter
    def width(self, value):
        self.__validate_num(
            -240, 240,
            lambda: setattr(self, "__width", value),
            value,
            "width"
        )

    @property
    def height(self) -> float:
        return self.__height
    
    @height.setter
    def height(self, value):
        self.__validate_num(
            -180, 180,
            lambda: setattr(self, "__height", value),
            value,
            "height"
        )
    
    @property
    def x(self) -> float:
        return self.__x
    
    @x.setter
    def x(self, value):
        self.__validate_num(
            -240, 240,
            lambda: setattr(self, "__x", value),
            value,
            "x-coordinate"
        )

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, value):
            self.__validate_num(
            -180, 180,
            lambda: setattr(self, "__y", value),
            value,
            "y-coordinate"
        )
    
    @property
    def is_visible(self) -> bool:
        return self.__visible
    
    @is_visible.setter
    def set_visible(self, value):
        if type(value) is bool:
            self.__visible = value
        else:
            raise TypeError(f"Monitor visibility must be a boolean value, but {value} of type {type(value)} was given.")

    # Re-serialize the monitor data
    def output(self) -> dict:
        return {
            "id": self.__id,
            "mode": self.__mode,
            "opcode": self.__opcode,
            "params": self.__params,
            "spriteName": self.__sprite_name,
            "value": self.__value,
            "width": self.__width,
            "height": self.__height,
            "x": self.__x,
            "y": self.__y,
            "visible": self.__visible,
        }
    
    @staticmethod
    def create_monitor(monitor_dict: dict) -> Monitor | VariableMonitor:
        """Decides whether to create a base Monitor or a VariableMonitor based on the input object."""
        if "sliderMin" in monitor_dict:
            return VariableMonitor(monitor_dict)
        else:
            return Monitor(monitor_dict)

class VariableMonitor(Monitor):
    def __init__(self, monitor_data) -> None:
        super().__init__(monitor_data)
        self.__slider_min = monitor_data["sliderMin"]
        self.__slider_max = monitor_data["sliderMax"]
        self.__is_discrete = monitor_data["isDiscrete"]

    @property
    def slider_min(self) -> float | int:
        return self.__slider_min

    @slider_min.setter
    def slider_min(self, value):
        self.__validate_num(
            -float("inf"), float("inf"),
            setattr(self, "__slider_min", value),
            value,
            "slider minimum"
        )

    @property
    def slider_max(self) -> float | int:
        return self.__slider_max

    @slider_max.setter
    def slider_max(self, value):
        self.__validate_num(
            -float("inf"), float("inf"),
            setattr(self, "__slider_max", value),
            value,
            "slider maximum"
        )

    @property
    def is_discrete(self) -> bool:
        return self.__is_discrete
    
    @is_discrete.setter
    def is_discrete(self, value):
        if type(value) is bool:
            self.__is_discrete = value

    def output(self) -> dict:
        return super().output() | {
            "sliderMin": self.__slider_min,
            "sliderMax": self.__slider_max,
            "isDiscrete": self.__is_discrete
        }