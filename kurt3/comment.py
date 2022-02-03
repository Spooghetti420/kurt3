from kurt3.has_id import IDObject, IDObjectManager


class CommentManager(IDObjectManager):
    def __init__(self, comment_dict) -> None:
        super().__init__(comment_dict, Comment)

class Comment(IDObject):
    def __init__(self, id, values) -> None:
        super().__init__(id)
        self.__block_id = values["blockId"]
        self.__x = values["x"]
        self.__y = values["y"]
        self.__width = values["width"]
        self.__height = values["height"]
        self.__minimized = values["minimized"]
        self.__text = values["text"]
    
    def output(self):
        return {
            "blockId": self.__block_id,
            "x": self.__x,
            "y": self.__y,
            "width": self.__width,
            "height": self.__height,
            "minimized": self.__minimized,
            "text": self.__text
        }