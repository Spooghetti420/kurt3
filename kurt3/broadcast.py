from kurt3.subject import IDObject, IDObjectManager


class BroadcastManager(IDObjectManager):
    def __init__(self, broadcast_dict) -> None:
        super().__init__(Broadcast, broadcast_dict)
    
class Broadcast(IDObject):
    def __init__(self, id, name) -> None:
        super().__init__(id)
        self.__name = name
    
    @property
    def name(self) -> str:
        """
        The name of the broadast.
        """
        return self.__name
    
    def output(self):
        return self.__name