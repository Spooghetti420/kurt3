from __future__ import annotations
from kurt3.block import BlockManager
from kurt3.broadcast import BroadcastManager
from kurt3.comment import CommentManager
from kurt3.costume import CostumeManager
from kurt3.lists import ListManager
from kurt3.sound import SoundManager
from kurt3.variable import VariableManager


class TargetManager:
    """
    Represents the list of all "targets" that belong to the project. A "target" is a general term
    for either the `Stage` or a `Sprite`.
    """
    def __init__(self, target_list) -> None:
        self.__targets: list[Target] = [Target.create_target(t) for t in target_list]
    
    def get_stage(self):
        try:
            return [t for t in self.__targets if t.is_stage][0]
        except IndexError:
            raise NameError("Stage object does not exist.")
    
    def output(self):
        return [t.output() for t in self.__targets]

class Target:
    """
    Represents a single "target", either a `Stage` or a `Sprite`. As a base class, this is not sufficient
    to represent either, as `Stage`s and `Sprite`s also both have unique properties. 
    """
    def __init__(self, target_dict) -> None:
        self.__is_stage = target_dict["isStage"]
        self.__name = target_dict["name"]
        self.__variables = VariableManager(target_dict["variables"])
        self.__lists = ListManager(target_dict["lists"])
        self.__broadcasts = BroadcastManager(target_dict["broadcasts"]) # There won't be any for a sprite, i.e. {}
        self.__blocks = BlockManager(target_dict["blocks"])
        self._comments = CommentManager(target_dict["comments"])
        self.__current_costume = target_dict["currentCostume"]
        self.__costumes = CostumeManager(target_dict["costumes"])
        self.__sounds = SoundManager(target_dict["sounds"])
        self.__layer_order = target_dict["layerOrder"]
        self.__volume = target_dict["volume"]

    @property
    def is_stage(self):
        """Whether the target is the Stage."""
        return self.__is_stage

    @property
    def name(self):
        """The name of the target."""
        return self.__name

    @name.setter
    def set_name(self, value: str):
        if type(value) is str:
            self.__name = value
        else:
            raise TypeError(f"Variable name must be a string, but {value} of type {type(value)} was received.")
    
    @property
    def variables(self) -> VariableManager:
        """
        The variables local to this target. Note that variables of the Stage are considered global variables.
        """
        return self.__variables
    
    @property
    def broadcasts(self) -> BroadcastManager:
        """
        The broadcasts this target references.
        """
        return self.__broadcasts
    
    @property
    def blocks(self) -> BlockManager:
        """
        The blocks contained within this target.
        """
        return self.__blocks
    
    @property
    def comments(self) -> CommentManager:
        """
        The comments in the code area for this target.
        """
        return self._comments
    
    @property
    def current_costume(self) -> CostumeManager:
        """
        This target's currently selected costume.
        """
        return self.__current_costume
    
    @current_costume.setter
    def set_costume(self, value):
        if type(value) is not int:
            raise TypeError(f"Costume number must be an integer, but {value} of type {type(value)} was received.")
        
        upper_bound = len(self.__costumes.costumes)
        if 0 < value <= upper_bound:
            self.__current_costume = value
        else:
            raise ValueError(f"Costume number ({value}) out of range: must be between 1 and {upper_bound} inclusive.")

    @property
    def costumes(self) -> CostumeManager:
        """
        The costumes that belong to this target.
        """
        return self.__costumes

    @property
    def sounds(self) -> SoundManager:
        """
        The sounds that belong to this target.
        """
        return self.__sounds
    
    @property
    def layer(self) -> int:
        """
        The order in Scratch's layer system that the target occupies.
        The lower this is, the farther back it appears. The stage is always assigned the special value 0.
        """
        return self.__layer_order

    @property
    def volume(self) -> float:
        """
        This target's volume. This applies to music blocks and sounds.
        """
        return self.__volume
    

    def output(self) -> dict:
        return {
            "isStage": self.__is_stage,
            "name": self.__name,
            "variables": self.__variables.output(),
            "lists": self.__lists.output(),
            "broadcasts": self.__broadcasts.output(),
            "blocks": self.__blocks.output(),
            "comments": self._comments.output(),
            "currentCostume": self.__current_costume,
            "costumes": self.__costumes.output(),
            "sounds": self.__sounds.output(),
            "volume": self.__volume,
            "layerOrder": self.__layer_order,
        }

    @staticmethod
    def create_target(target_dict: dict) -> Stage | Sprite:
        """
        Creates either a `Stage` or a `Sprite` object, depending on value of the
        `isStage` attribute.
        """

        if target_dict["isStage"]:
            return Stage(target_dict)
        else:
            return Sprite(target_dict)


class Stage(Target):
    """
    Represents the Stage of a project. Beyond typical `Target` properties, a `Stage`
    also has `tempo`, `video_transparency`, `video_state`, and `tts_language`.
    """
    def __init__(self, target_dict) -> None:
        super().__init__(target_dict)
        self.__tempo = target_dict["tempo"]
        self.__video_transparency = target_dict["videoTransparency"]
        self.__video_state = target_dict["videoState"]
        self.__tts_language = target_dict["textToSpeechLanguage"]

    @property
    def tempo(self) -> int:
        """
        The stage's tempo, used for music blocks.
        """
        return self.__tempo
    
    @property
    def video_transparency(self):
        """
        The transparency of the video when using the video extension.
        Apparently applied to all new projects, regardless of whether they use this extension.
        """
        return self.__video_transparency

    @property
    def video_state(self) -> str:
        """
        Whether the video is `on` or `off`.
        """
        return self.__video_state

    @property
    def tts_language(self):
        """
        The current text-to-speech language when using the text-to-speech extension,
        ostensibly represented using an ISO 639-1 language code, e.g. `ja`, `ar`, etc.
        """
        return self.__tts_language
    
    def output(self) -> dict:
        return super().output() | {
                "tempo": self.__tempo,
                "videoTransparency": self.__video_transparency,
                "videoState": self.__video_state,
                "textToSpeechLanguage": self.__tts_language
            }

class Sprite(Target):
    """
    Represents a sprite within the project. As it is a dynamic element, it also has
    attributes such as `x` and `y`, `visible`, `size`, `direction`, `draggable`, and `rotation_style`.
    """
    def __init__(self, target_dict) -> None:
        super().__init__(target_dict)
        self.__visible = target_dict["visible"]
        self.__x = target_dict["x"]
        self.__y = target_dict["y"]
        self.__size = target_dict["size"]
        self.__direction = target_dict["direction"]
        self.__draggable = target_dict["draggable"]
        self.__rotation_style = target_dict["rotationStyle"]
    
    @property
    def is_visible(self) -> bool:
        """
        Whether the sprite is currently visible or not. This is toggled in Scratch using the eye icon,
        as well as the "hide" and "show" blocks.
        """
        return self.__visible
    
    @property
    def x(self) -> float:
        """
        The x-coordinate on the Stage of the sprite. 
        """
        return self.__x
    
    @property
    def y(self) -> float:
        """
        The y-coordinate on the Stage of the sprite.
        """
        return self.__y
    
    @property
    def size(self):
        """
        The sprite's current size, as a percentage.
        """
        return self.__size
    
    @property
    def direction(self) -> float:
        """
        The direction (heading) of the sprite, in degrees.
        """
        return self.__direction
    
    @property
    def is_draggable(self):
        return self.__draggable
    
    @property
    def rotation_style(self) -> str:
        """
        The sprite's rotation style, e.g. "all-around".
        """
        return self.__rotation_style

    def output(self) -> dict:
        return super().output() | {
                "visible": self.__visible,
                "x": self.__x,
                "y": self.__y,
                "size": self.__size,
                "direction": self.__direction,
                "draggable": self.__draggable,
                "rotationStyle": self.__rotation_style
            }