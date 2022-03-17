from typing import Tuple
from kurt3.block import Block
from kurt3.blocks.input_slot import InputSlotNumeric
from kurt3.project import Project

STYLES = {
    "LEFT_RIGHT": "left-right",
    "DONT_ROTATE": "don't rotate",
    "ALL_AROUND": "all around"
}

def MoveSteps(project: Project, steps = 10) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_movesteps",
        inputs = {
            "STEPS": InputSlotNumeric(steps)
        }
    )

def TurnRight(project: Project, degrees = 15) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_turnright",
        inputs = {
            "DEGREES": InputSlotNumeric(degrees)
        }
    )


def TurnLeft(project: Project, degrees = 15) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_turnleft",
        inputs = {
            "DEGREES": InputSlotNumeric(degrees)
        }
    )

def GoToMenu(project: Project, goto: str = "_random_") -> Block:
    """
    A go-to block which accepts a sprite name to go to,
    or "_random_" or "_mouse_" to access a random position
    or the mouse position.
    """
    return Block (
        id = project.generate_id(),
        opcode = "motion_goto_menu",
        fields = {
            "TO": [
                "_mouse_",
                None
            ]
        }
    )

def GoToXY(project: Project, x = 0, y = 0) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_gotoxy",
        inputs = {
            "X": InputSlotNumeric(x),
            "Y": InputSlotNumeric(y)
        }
    )

def GlideSecsToXY(project: Project, secs = 1, x = 0, y = 0) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_glidesecstoxy",
        inputs = {
                "SECS": InputSlotNumeric(secs),
                "X": InputSlotNumeric(x),
                "Y": InputSlotNumeric(y)
            }
        )

def GlideSecsToMenu(project: Project, secs = 1, goto: str = "_random_", sprite = None) -> Tuple[Block, Block]:
    id1 = project.generate_id()
    id2 = project.generate_id()

    glide_to = Block (
        id = id1,
        opcode = "motion_glideto",
        inputs = {
                "SECS": InputSlotNumeric(secs),
                "TO": [
                    1,
                    id2
                ]
            }
        )
 
    glide_to_menu = GlideToMenu(project, goto, id1, id2)
    return (glide_to, glide_to_menu)

def GlideToMenu(project: Project, goto: str, id1: str, id2: str) -> Block:
    return Block (
        id = id2,
        opcode = "motion_glideto_menu",
        fields = { 
            "TO": [
                    goto,
                    None
                ]
            },
        parent = id1,
        topLevel = False,
        shadow = True
    )

def GlideSecsToXY(project: Project, secs = 1, x = 0, y = 0) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_glidesecstoxy",
        inputs = {
                "SECS": InputSlotNumeric(secs),
                "X": InputSlotNumeric(x),
                "Y": InputSlotNumeric(y)
            }
        )

def PointInDirection(project: Project, degrees = 90) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_pointindirection",
        inputs = {
            "DIRECTION": InputSlotNumeric(degrees)
        }

    )
        
def ChangeXBy(project: Project, dx = 10) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_changexby",
        inputs = {
            "DX": InputSlotNumeric(dx)
        }
    )

def ChangeYBy(project: Project, dy = 10) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_changeyby",
        inputs = {
            "DY": InputSlotNumeric(dy)
        }
    )

def SetX(project: Project, x = 0) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_setx",
        inputs = {
            "X": InputSlotNumeric(x)
        }
    )

def SetY(project: Project, y = 0) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_sety",
        inputs = {
            "Y": InputSlotNumeric(y)
        }
    )

def IfOnEdgeBounce(project: Project) -> Block:
    return Block (
        id = project.generate_id(),
        opcode = "motion_ifonedgebounce"
    )

def SetRotationStyle(project: Project, style: str = "all around") -> Block:
    if style not in STYLES.values():
        raise ValueError(f"Rotation style must be one of: {', '.join(STYLES)}, but `{style}` was received.")

    return Block (
        id = project.generate_id(),
        opcode = "motion_setrotationstyle",
        fields = {
            "STYLE": [
                style,
                None
            ]
        }
    )

def XPosition(project: Project):
    return Block (
        id = project.generate_id(),
        opcode = "motion_xposition",
    )

def YPosition(project: Project):
    return Block (
        id = project.generate_id(),
        opcode = "motion_yposition",
    )

def Direction(project: Project):
    return Block (
        id = project.generate_id(),
        opcode = "motion_direction",
    )