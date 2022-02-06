from __future__ import annotations#

from kurt3.subject import HasWidthHeight, HasXY, Subject

class MonitorManager:
    def __init__(self, monitor_list) -> None:
        self.__monitors = [Monitor.create_monitor(m) for m in monitor_list]
    
    @property
    def monitors(self) -> list[Monitor]:
        """
        A list of all variable and list monitors in this project,
        given as `Monitor` objects.
        """
        return self.__monitors

    def by_name(self, name):
        """
        Search for a monitor which monitors a given variable / list by its name."""
        return [m for m in self.__monitors if m.name == name][0]

    def by_id(self, id):
        """
        Search for a monitor which monitors a given variable / list by its ID.
        """
        return [m for m in self.__monitors if m.id == id][0]

    def output(self) -> list[Monitor]:
        return [m.output() for m in self.__monitors]

class Monitor(HasXY, HasWidthHeight):
    """
    Class that represents
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
        self._width = monitor_data["width"]
        self._height = monitor_data["height"]
        self._x = monitor_data["x"]
        self._y = monitor_data["y"]
        self.__visible = monitor_data["visible"]

    @property
    def id(self) -> str:
        """
        Returns the ID of the variable this monitor is displaying.
        """
        return self.__id
    
    @property
    def mode(self) -> str:
        """
        Returns a string that represents what kind of monitoring this monitor is doing.
        For lists, this is `list`, and for variables can be e.g. `default`.
        """
        return self.__mode
    
    @property
    def opcode(self) -> str:
        """
        The underlying internal opcode of the monitor type.
        List would return `data_listcontents`, and variable `data_variable`.
        """
        return self.__opcode
    
    @property
    def params(self) -> dict:
        """
        This is a dictionary which contains a key (either `VARIABLE` or `LIST`), and whose
        corresponding value is the variable name.
        """
        return self.__params
    
    @property
    def name(self) -> str | None:
        """
        Returns the variable or list name, as derived from `self.params`.
        If not applicable, as some non-list/variable monitors have no such property,
        this will return `None`.
        """
        
        if self.__opcode in ("data_variable", "data_listcontents"): 
            return list(self.params.values())[0]
    
    @property
    def sprite_name(self) -> str | None:
        """
        Returns the sprite name of the variable or list this monitor belongs
        to, or `None` if the monitor belongs to the stage.
        """
        return self.__sprite_name
    
    @property
    def value(self) -> int | float | str:
        """
        The value displayed on this monitor.
        """
        return self.__value
    
    @property
    def is_visible(self) -> bool:
        """
        Whether the monitor has been made visible
        to the user.
        """
        return self.__visible
    
    @is_visible.setter
    def is_visible(self, value):
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
            "width": self._width,
            "height": self._height,
            "x": self._x,
            "y": self._y,
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
        """
        The minimum value of the variable monitor
        when set to slider mode. The slider mode allows the user
        to set the variable's value to between this lower bound and the
        slider's maximum while viewing the project.
        """
        return self.__slider_min

    @slider_min.setter
    def slider_min(self, value):
        self._validate_num(
            -float("inf"), float("inf"),
            setattr(self, "__slider_min", value),
            value,
            "slider minimum"
        )

    @property
    def slider_max(self) -> float | int:
        """
        The maximum value of the variable monitor
        when set to slider mode. The slider mode allows the user
        to set the variable's value to between the slider's lower bound and
        the this upper bound while viewing the project.
        """
        return self.__slider_max

    @slider_max.setter
    def slider_max(self, value):
        self._validate_num(
            -float("inf"), float("inf"),
            setattr(self, "__slider_max", value),
            value,
            "slider maximum"
        )

    @property
    def is_discrete(self) -> bool:
        """
        Whether the slider moves in discrete increments or continuous.
        """
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