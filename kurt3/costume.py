from __future__ import annotations
import os

from kurt3.asset import Asset


class CostumeManager:
    def __init__(self, costume_list: list[dict]) -> None:
        self.__costumes = [Costume.create_costume(c) for c in costume_list]
    
    @property
    def costumes(self):
        return self.__costumes

    def _add(self, md5_hash: str, name: str, extension: str, rotation_center = (0, 0)):
        self.__costumes.append(Costume.create_costume(
            {
                "assetId": md5_hash,
                "name": name,
                "md5ext": md5_hash + extension,
                "dataFormat": extension[1:],
                "rotationCenterX": rotation_center[0],
                "rotationCenterY": rotation_center[1],
                "bitmapResolution": 1
            }
        ))

    def output(self):
        return [c.output() for c in self.__costumes]
    
class Costume(Asset):
    def __init__(self, values: dict) -> None:
        super().__init__(values)
        self.__rotation_center_x = values["rotationCenterX"]
        self.__rotation_center_y = values["rotationCenterY"]
    
    @staticmethod
    def create_costume(values):
        if "bitmapResolution" in values:
            return BitmapCostume(values)
        else:
            return Costume(values)

    @property
    def rotation_center(self) -> tuple[float, float]:
        """
        The center of rotation of the image about which it is rotated when rotations are applied to it in Scratch.
        Returns a tuple containing the (x, y) coordinates of the center of rotation.
        """

    def output(self) -> dict:
        return super().output() | {
            "rotationCenterX": self.__rotation_center_x,
            "rotationCenterY": self.__rotation_center_y
        }

class BitmapCostume(Costume):
    def __init__(self, values: dict) -> None:
        super().__init__(values)
        self.__bitmap_resolution = values["bitmapResolution"]

    @property
    def bitmap_resolution(self):
        """
        Tentatively unclear what this refers to. Some images have a resolution of 1, others of 2.
        At any rate, returns the bitmap costume's `bitmapResolution`.
        """

    def output(self) -> dict:
        return super().output() | {
            "bitmapResolution": self.__bitmap_resolution
        }