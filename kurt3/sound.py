class SoundManager:
    def __init__(self, sound_list: list[dict]) -> None:
        self.__sounds = [Sound(s) for s in sound_list]
    
    def output(self):
        return [s.output() for s in self.__sounds]
    
class Sound:
    def __init__(self, values: dict) -> None:
        self.__asset_id = values["assetId"]
        self.__name = values["name"]
        self.__data_format = values["dataFormat"]
        self.__format = values["format"]
        self.__rate = values["rate"]
        self.__sample_count = values["sampleCount"]
        self.__md5_ext = values["md5ext"]

    def output(self):
        return {
            "assetId": self.__asset_id,
            "name": self.__name,
            "dataFormat": self.__data_format,
            "format": self.__format,
            "rate": self.__rate,
            "sampleCount": self.__sample_count,
            "md5ext": self.__md5_ext
        }