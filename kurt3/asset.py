class Asset:
    def __init__(self, values: dict) -> None:
        self.__asset_id = values["assetId"]
        self.__name = values["name"]
        self.__data_format = values["dataFormat"]
        self.__md5_ext = values["md5ext"]

    @property
    def asset_id(self) -> str:
        """
        The "ID" of the asset. This is always the md5 hash of the file data of the asset file.
        """
        return self.__asset_id

    @property
    def md5_with_extension(self) -> str:
        """
        The md5 hash (asset ID) + the file extension of the asset's data file within the project.
        This uniquely identifies the asset within the .sb3 file (which is a zip archive, in fact).
        """
        return self.__md5_ext
    
    @property
    def data_format(self) -> str:
        """
        Effectively the filetype of the asset. Example values include `svg`, `png`, `wav`, etc.
        """
        return self.__data_format

    def output(self) -> dict:
        return {
            "assetId": self.__asset_id,
            "name": self.__name,
            "md5ext": self.__md5_ext,
            "dataFormat": self.__data_format
        }