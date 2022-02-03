class CostumeManager:
    def __init__(self, costume_list: list[dict]) -> None:
        self.__costumes = [Costume.create_costume(c) for c in costume_list]
    
    def output(self):
        return [c.output() for c in self.__costumes]
    
class Costume:
    def __init__(self, values: dict) -> None:
        self.__asset_id = values["assetId"]
        self.__name = values["name"]
        self.__md5_ext = values["md5ext"]
        self.__data_format = values["dataFormat"]
        self.__rotation_center_x = values["rotationCenterX"]
        self.__rotation_center_y = values["rotationCenterY"]
    
    @staticmethod
    def create_costume(values):
        if "bitmapResolution" in values:
            return BitmapCostume(values)
        else:
            return Costume(values)

    def output(self) -> dict:
        return {
            "assetId": self.__asset_id,
            "name": self.__name,
            "md5ext": self.__md5_ext,
            "dataFormat": self.__data_format,
            "rotationCenterX": self.__rotation_center_x,
            "rotationCenterY": self.__rotation_center_y
        }

class BitmapCostume(Costume):
    def __init__(self, values: dict) -> None:
        super().__init__(values)
        self.__bitmap_resolution = values["bitmapResolution"]

    def output(self) -> dict:
        return super().output() | {
            "bitmapResolution": self.__bitmap_resolution
        }