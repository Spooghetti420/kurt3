from kurt3.block import Block
from kurt3.blocks.input_slot import InputSlotNumeric
from kurt3.target import Target

class MoveSteps(Block):
    def __init__(self, steps = 10) -> None:
        super().__init__(
            opcode = "motion_movesteps",
            inputs = {
            "STEPS": InputSlotNumeric(steps)
            }
        )


class TurnRight(Block):
    def __init__(self, degrees = 15) -> None:
        super().__init__(
            opcode = "motion_turnright",
            inputs = {
                "DEGREES": InputSlotNumeric(degrees)
            }
        )


class TurnLeft(Block):
    def __init__(self, degrees = 15) -> None:
        super().__init__(
            opcode = "motion_turnleft",
            inputs = {
                "DEGREES": InputSlotNumeric(degrees)
            }
        )

class GoToMenu(Block):
    def __init__(self, goto: str = "_random_") -> None:
        """
        A go-to block which accepts a sprite name to go to,
        or "_random_" or "_mouse_" to access a random position
        or the mouse position.
        """
        super().__init__(
            opcode = "motion_goto_menu",
            fields = {
                "TO": [
                    "_mouse_",
                    None
                ]
            }
        )

class GoToXY(Block):
    def __init__(self, x = 0, y = 0) -> None:
        super().__init__(
            opcode = "motion_gotoxy",
            inputs = {
                "X": InputSlotNumeric(x),
                "Y": InputSlotNumeric(y)
            }
        )

class GlideSecsToXY(Block):
    def __init__(self, secs = 1, x = 0, y = 0) -> None:
        super().__init__(
            opcode = "motion_glidesecstoxy",
            inputs = {
                    "SECS": InputSlotNumeric(secs),
                    "X": InputSlotNumeric(x),
                    "Y": InputSlotNumeric(y)
                }
            )

class GlideSecsToMenu(Block):
    def __init__(self, sprite: Target, secs = 1, goto: str = "_random_") -> None:
        super().__init__(
            opcode = "motion_glideto",
            # inputs = {
            #         "SECS": InputSlotNumeric(secs),
            #         "TO": [
            #             1,
            #             child._id
            #         ]
            #     }
            )

class GlideToMenu(Block):
    def __init__(self, goto: str = "_random_") -> None:
        super().__init__(
            opcode = "motion_glideto_menu",
            fields = { 
                "TO": [
                        goto,
                        None
                    ]
                }
            )

class GlideSecsToXY(Block):
    def __init__(self, secs = 1, x = 0, y = 0) -> None:
        super().__init__(
            opcode = "motion_glidesecstoxy",
            inputs = {
                    "SECS": InputSlotNumeric(secs),
                    "X": InputSlotNumeric(x),
                    "Y": InputSlotNumeric(y)
                }
            )

class PointInDirection(Block):
    def __init__(self, degrees = 90) -> None:
        super().__init__(
            opcode = "motion_pointindirection",
            inputs = {
                "DIRECTION": InputSlotNumeric(degrees)
            }

        )
        
class ChangeXBy(Block):
    def __init__(self, dx = 10) -> None:
        super().__init__(
            opcode = "motion_changexby",
            inputs = {
                "DX": InputSlotNumeric(dx)
            }
        )

class ChangeYBy(Block):
    def __init__(self, dy = 10) -> None:
        super().__init__(
            opcode = "motion_changeyby",
            inputs = {
                "DY": InputSlotNumeric(dy)
            }
        )

class SetX(Block):
    def __init__(self, x = 0) -> None:
        super().__init__(
            opcode = "motion_setx",
            inputs = {
                "X": InputSlotNumeric(x)
            }
        )
        

class SetY(Block):
    def __init__(self, y = 0) -> None:
        super().__init__(
            opcode = "motion_sety",
            inputs = {
                "Y": InputSlotNumeric(y)
            }
        )

class IfOnEdgeBounce(Block):
    def __init__(self) -> None:
        super().__init__(
            opcode = "motion_ifonedgebounce"
        )

class SetRotationStyle(Block):
    STYLES = {
        "left-right",
        "don't rotate",
        "all around"
    }
    def __init__(self, style: str = "all around") -> None:
        # if style not in SetRotationStyle.STYLES:
        #     raise ValueError(f"Rotation style must be one of: {', '.join(SetRotationStyle.STYLES)}, but `{style}` was received.")
        super().__init__(
            opcode = "motion_setrotationstyle",
            fields = {
                "STYLE": [
                    style,
                    None
                ]
            }
        )

class XPosition(Block):
    def __init__(self) -> None:
        super().__init__(
            opcode = "motion_xposition",
        )

class YPosition(Block):
    def __init__(self) -> None:
        super().__init__(
            opcode = "motion_yposition",
        )

class Direction(Block):
    def __init__(self) -> None:
        super().__init__(
            opcode = "motion_direction",
        )



