from kurt3.block import Block
from kurt3.blocks.input_slot import InputSlotNumeric

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
            opcode="motion_turnright",
            inputs={
                "DEGREES": InputSlotNumeric(degrees)
            }
        )


class TurnLeft(Block):
    def __init__(self, degrees = 15) -> None:
        super().__init__(
            opcode="motion_turnleft",
            inputs={
                "DEGREES": InputSlotNumeric(degrees)
            }
        )

class GoToXY(Block):
    def __init__(self, x = 0, y = 0) -> None:
        super().__init__(
            opcode="motion_gotoxy",
            inputs= {
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
            opcode = "motion_changexby",
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
        