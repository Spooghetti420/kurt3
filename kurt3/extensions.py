EXTENSIONS = {
    "TextToSpeech": "text2speech",
    "Music": "music",
    "Pen": "pen",
    "Video": "videoSensing",
    "Translation": "translate",
    "MakeyMakey": "makeymakey",
    "Boost": "boost",
    "EV3": "ev3",
    "MicroBit": "microbit",
    "WeDo": "wedo2",
    "GDXFor": "gdxfor"
    }

class ExtensionManager:
    def __init__(self, extension_list: list[str]) -> None:
        self.__extensions = set(extension_list)

        for ext in extension_list:
            if ext not in EXTENSIONS.values():
                raise ValueError(f"Error loading project: Project contains invalid extension {ext}.")
    
    @property
    def extensions(self):
        return self.__extensions
    
    def add_extension(self, ext) -> None:
        if ext in EXTENSIONS:
            self.__extensions.add(EXTENSIONS[ext])
        elif ext in EXTENSIONS.values():
            self.__extensions.add(ext)
        else:
            raise ValueError(f"Failed to add extension {ext} to project: extension does not exist.")
        
    def remove_extension(self, ext) -> None:
        if ext in EXTENSIONS and EXTENSIONS[ext] in self.__extensions:
            self.__extensions.remove(EXTENSIONS[ext])
        elif ext in EXTENSIONS.values() and EXTENSIONS[ext] in self.__extensions:
            self.__extensions.remove(ext)
        else:
            raise Warning(f"Warning: attempted to remove extension {ext}; extension was not already in the project.")
    
    def output(self) -> list[str]:
        return list(self.__extensions)