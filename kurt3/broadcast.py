from kurt3.has_id import IDObject, IDObjectManager


class BroadcastManager(IDObjectManager):
    def __init__(self, broadcast_dict) -> None:
        super().__init__(broadcast_dict, Broadcast)
    
class Broadcast(IDObject):
    def __init__(self, id, name) -> None:
        super().__init__(id)
        self.__name = name
    
    @property
    def name(self):
        return self.__name
    
    def output(self):
        return self.__name