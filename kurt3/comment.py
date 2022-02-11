from kurt3.subject import IDObject, IDObjectManager


class CommentManager(IDObjectManager):
    def __init__(self, comment_dict) -> None:
        super().__init__(Comment, comment_dict)

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

    @property
    def block_id(self) -> str:
        """
        The ID of the block that this comment refers to.
        """
        return self.__block_id
    
    @property
    def x(self) -> float:
        """
        The x-coordinate of this comment.
        """
        return self.__x

    @property
    def y(self) -> float:
        """
        The y-coordinate of this comment.
        """
        return self.__y

    @property
    def width(self) -> float:
        """
        The width of the comment box.
        """
        return self.__width

    @property
    def height(self) -> float:
        """
        The height of the comment box.
        """
        return self.__height

    @property
    def is_minimized(self) -> bool:
        """
        Whether the comment box is minimized. This shortens the comment text
        in the visual editor down to a few characters.
        """
        return self.__minimized

    @property
    def text(self) -> str:
        """
        Return the comment's text.
        """
        return self.__text

    @text.setter
    def set_text(self, value):
        if type(value) is not str:
            raise TypeError(f"Comment must be of type string, but {value} of type {type(value)} was received.")

        self.__text = value

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