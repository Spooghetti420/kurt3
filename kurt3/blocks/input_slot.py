from __future__ import annotations

def InputSlotFloat(num: float):
    return [
        1,
        [
            4,
            str(num)
        ]
    ]

def InputSlotInt(num: int):
    return [
        1,
        [
            7,
            str(num)
        ]
    ]

def InputSlotString(string: str):
    return [
        1,
        [
            10,
            str("Hello!")
        ]
    ]

def InputSlotID(ID: str):
    return [
        1,
        str(ID)
    ]