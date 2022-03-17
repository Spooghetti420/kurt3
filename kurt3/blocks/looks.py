from typing import Tuple
from kurt3.block import Block
from kurt3.blocks.input_slot import InputSlotFloat, InputSlotID, InputSlotInt, InputSlotString
from kurt3.project import Project


def SayForSecs(project: Project, secs = 2, message = "Hello!") -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_sayforsecs",
        inputs = {
            "MESSAGE": InputSlotString(message),
            "SECS": InputSlotFloat(secs)
        }
    )

def Say(project: Project, message = "Hello!") -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_say",
        inputs = {
            "MESSAGE": InputSlotString(message),
        }
    )

def ThinkForSecs(project: Project, secs = 2, message = "Hmm...") -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_thinkforsecs",
        inputs = {
            "MESSAGE": InputSlotString(message),
            "SECS": InputSlotFloat(secs)
        }
    )

def Think(project: Project, message = "Hmm...") -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_think",
        inputs = {
            "MESSAGE": InputSlotString(message),
        }
    )

def ThinkForSecs(project: Project, secs = 2, message = "Hmm...") -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_thinkforsecs",
        inputs = {
            "MESSAGE": InputSlotString(message),
            "SECS": InputSlotFloat(secs)
        }
    )

def SwitchCostumeTo(project: Project, costume: str) -> Tuple[Block, Block]:
    id1 = project.generate_id()
    id2 = project.generate_id()

    switch_costume_to = Block (
        id = id1,
        opcode = "looks_switchcostumeto",
        inputs = {
                "COSTUME": [
                    1,
                    id2
                ]
            }
        )

    costume_dropdown = CostumeDropdown(costume, id1, id2)
    return (switch_costume_to, costume_dropdown)
 
def CostumeDropdown(costume_name: str, id1: str, id2: str) -> Block:
    return Block (
        id = id2,
        opcode = "looks_costume",
        fields = { 
            "COSTUME": [
                    str(costume_name),
                    None
                ]
            },
        parent = id1,
        topLevel = False,
        shadow = True
    )

def NextCostume(project: Project) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_nextcostume"
    )

def SwitchBackdropTo(project: Project, backdrop: str = "backdrop1") -> Block:
    id1 = project.generate_id()
    id2 = project.generate_id()

    switch_backdrop_to = Block (
        id = id1,
        opcode = "looks_switchbackdropto",
        inputs = {
            "BACKDROP": InputSlotID(id2)
        }
    )

    backdrop_dropdown = BackdropDropdown(backdrop, id1, id2)
    return (switch_backdrop_to, backdrop_dropdown)

def BackdropDropdown(backdrop_name: str, id1: str, id2: str) -> Block:
    return Block (
        id = id2,
        opcode = "looks_backdrops",
        fields = { 
            "BACKDROP": [
                    str(backdrop_name),
                    None
                ]
            },
        parent = id1,
        topLevel = False,
        shadow = True
    )

def NextBackdrop(project: Project) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_nextbackdrop"
    )

def ChangeSizeBy(project: Project, percentage: float = 10) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_changesizeby",
        inputs = {
            "CHANGE": InputSlotFloat(percentage),
        }
    )

def SetSizeTo(project: Project, percentage: float = 100) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_setsizeto",
        inputs = {
            "SIZE": InputSlotFloat(percentage),
        }
    )

def ChangeEffectBy(project: Project, effect_type: str, percentage: float = 25) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_changeeffectby",
        inputs = {
            "CHANGE": InputSlotFloat(percentage),
        },
        fields = {
            "EFFECT": [
                effect_type,
                None
            ]
        }
    )

def SetEffectTo(project: Project, effect_type: str, percentage: float = 25) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_seteffectto",
        inputs = {
            "VALUE": InputSlotFloat(percentage),
        },
        fields = {
            "EFFECT": [
                effect_type,
                None
            ]
        }
    )

def ClearGraphicsEffects(project: Project) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_cleargraphiceffects"
    )


def Show(project: Project) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_show"
    )

def Hide(project: Project) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_hide"
    )

def GoToFrontBack(project: Project, front_back: str) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_gotofrontback",
        fields = {
            "FRONT_BACK": [
                front_back,
                None
            ]
        }
    )

def GoForwardBackwardLayers(project: Project, forward_backward: str, number_of_layers: int = 1) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_goforwardbackwardlayers",
        inputs = {
            "NUM": InputSlotInt(number_of_layers)
        },
        fields = {
            "FORWARD_BACKWARD": [
                forward_backward,
                None
            ]
        }
    )

def CostumeNumberName(project: Project, number_name: str):
    return Block (
        id = project.generate_id(),
        opcode = "looks_costumenumbername",
        fields = {
            "NUMBER_NAME": [
                number_name,
                None
            ]
        }
    )

def BackdropNumberName(project: Project, number_name: str):
    return Block (
        id = project.generate_id(),
        opcode = "looks_backdropnumbername",
        fields = {
            "NUMBER_NAME": [
                number_name,
                None
            ]
        }
    )

def Size(project: Project) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "looks_size"
    )