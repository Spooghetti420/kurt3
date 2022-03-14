from __future__ import annotations
from kurt3.block import Block, BlockManager
from kurt3.broadcast import BroadcastManager
from kurt3.comment import CommentManager
from kurt3.costume import Costume, CostumeManager
from kurt3.lists import ListManager
from kurt3.sound import SoundManager
from kurt3.subject import HasXY
from kurt3.variable import VariableManager


class TargetManager:
    """
    Represents the list of all "targets" that belong to the project. A "target" is a general term
    for either the `Stage` or a `Sprite`.
    """
    def __init__(self, target_list, project=None) -> None:
        self.__targets: list[Target] = [TargetManager.create_target(t, project=project) for t in target_list]

    @staticmethod
    def create_target(target_dict: dict, project=None) -> Stage | Sprite:
        """
        Creates either a `Stage` or a `Sprite` object, depending on value of the
        `isStage` attribute.
        """

        # args = target_dict | {"project": project}
        if target_dict["isStage"]:
            return Stage(**target_dict, project=project)
        else:
            return Sprite(**target_dict, project=project)
    
    def get_stage(self):
        try:
            return [t for t in self.__targets if t.is_stage][0]
        except IndexError:
            raise NameError("Stage object does not exist.")

    def get_sprite_by_name(self, name) -> Target:
        try:
            return [t for t in self.__targets if t.name == name and not t.is_stage][0]
        except:
            raise NameError(f"The sprite with name {name} does not exist.")

    def as_list(self):
        return self.__targets
    
    def output(self):
        return [t.output() for t in self.__targets]

class Target:
    """
    Represents a single "target", either a `Stage` or a `Sprite`. As a base class, this is not sufficient
    to represent either, as `Stage`s and `Sprite`s also both have unique properties. 
    """
    def __init__(self,
        isStage = False,
        name = None,
        variables = {},
        lists = {},
        broadcasts = {},
        blocks = {},
        comments = {},
        currentCostume = 1,
        costumes = [],
        sounds = [],
        layerOrder = None,
        volume = 100,
        project = None
    ) -> None:
        self.__is_stage = isStage
        self.__name = name
        if name is None:
            raise Warning("Name was not assigned to target, saving cannot commence unless a unique name is chosen.")
        self.__variables = VariableManager(variables)
        self.__lists = ListManager(lists)
        self.__broadcasts = BroadcastManager(broadcasts)
        self.__blocks = BlockManager(blocks)
        self._comments = CommentManager(comments)
        self.__current_costume = currentCostume
        self.__costumes = CostumeManager(costumes, project)
        self.__sounds = SoundManager(sounds, project)
        self.__layer_order = layerOrder
        if layerOrder is None:
            raise Warning("Layer order was not assigned to target, saving cannot commence until a unique layer is selected.")
        self.__volume = volume
        self._project = project

    @property
    def is_stage(self):
        """Whether the target is the Stage."""
        return self.__is_stage

    @property
    def name(self):
        """The name of the target."""
        return self.__name

    @name.setter
    def name(self, value: str):
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
    def lists(self) -> ListManager:
        """
        The lists local to this target. Note that variables of the Stage are considered global.
        """
        return self.__lists
    
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

    def add_block(self, block: Block) -> Block:
        if block._id is None:
            block._id = self._project.generate_id(20)
        self.__blocks.add_block(block)
        return block

    def add_costume(self, file_path, costume_name, rotation_center = (0, 0)):
        # Check whether costume of this name exists already
        if bool([c for c in self.__costumes.costumes if c.name == costume_name]):
            raise ValueError(f"The chosen costume name ({costume_name}) already exists on this Target. Please choose a different one.")
        self.__costumes.add(file_path, costume_name, rotation_center)

    def add_sound(self, file_path, sound_name):
        if bool([s for s in self.__sounds.sounds if s.name == sound_name]):
            raise ValueError(f"The chosen sound name ({sound_name}) already exists on this Target. Please choose a different one.")
        self.__sounds.add(file_path, sound_name)

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


class Stage(Target):
    """
    Represents the Stage of a project. Beyond typical `Target` properties, a `Stage`
    also has `tempo`, `video_transparency`, `video_state`, and `tts_language`.
    """
    def __init__(self,
        tempo = 60,
        videoTransparency = 50,
        videoState = "on",
        textToSpeechLanguage = "en",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.__tempo = tempo
        self.__video_transparency = videoTransparency
        self.__video_state = videoState
        self.__tts_language = textToSpeechLanguage

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

class Sprite(Target, HasXY):
    """
    Represents a sprite within the project. As it is a dynamic element, it also has
    attributes such as `x` and `y`, `visible`, `size`, `direction`, `draggable`, and `rotation_style`.
    """
    def __init__(self,
        visible = True,
        x = 0,
        y = 0,
        size = 100,
        direction = 90,
        draggable = False,
        rotationStyle = "all around",
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.__visible = visible
        self._x = x
        self._y = y
        self.__size = size
        self.__direction = direction
        self.__draggable = draggable
        self.__rotation_style = rotationStyle
    
    @property
    def is_visible(self) -> bool:
        """
        Whether the sprite is currently visible or not. This is toggled in Scratch using the eye icon,
        as well as the "hide" and "show" blocks.
        """
        return self.__visible
    
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
                "x": self._x,
                "y": self._y,
                "size": self.__size,
                "direction": self.__direction,
                "draggable": self.__draggable,
                "rotationStyle": self.__rotation_style
            }