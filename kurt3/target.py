from kurt3.block import BlockManager
from kurt3.broadcast import BroadcastManager
from kurt3.comment import CommentManager
from kurt3.costume import CostumeManager
from kurt3.lists import ListManager
from kurt3.sound import SoundManager
from kurt3.variable import VariableManager


class TargetManager:
    def __init__(self, target_list) -> None:
        self.__targets: list[Target] = [Target.create_target(t) for t in target_list]

    def output(self):
        return [t.output() for t in self.__targets]

class Target:
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

    def create_target(target_dict: dict):
        if target_dict["isStage"]:
            return Stage(target_dict)
        else:
            return Sprite(target_dict)


class Stage(Target):
    def __init__(self, target_dict) -> None:
        super().__init__(target_dict)
        self.__tempo = target_dict["tempo"]
        self.__video_transparency = target_dict["videoTransparency"]
        self.__video_state = target_dict["videoState"]
        self.__tts_language = target_dict["textToSpeechLanguage"]
    
    def output(self) -> dict:
        return super().output() | {
                "tempo": self.__tempo,
                "videoTransparency": self.__video_transparency,
                "videoState": self.__video_state,
                "textToSpeechLanguage": self.__tts_language
            }

class Sprite(Target):
    def __init__(self, target_dict) -> None:
        super().__init__(target_dict)
        self.__visible = target_dict["visible"]
        self.__x = target_dict["x"]
        self.__y = target_dict["y"]
        self.__size = target_dict["size"]
        self.__direction = target_dict["direction"]
        self.__draggable = target_dict["draggable"]
        self.__rotation_style = target_dict["rotationStyle"]

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