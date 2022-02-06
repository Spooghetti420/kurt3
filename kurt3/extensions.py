from kurt3.subject import Manager


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

class ExtensionManager(Manager):
    """
    Represents the set of extensions of a project.
    Underlying extension names in Scratch are simple strings, but only a certain few correspond to a real
    extension. This supports adding and removing extensions from the project programmatically.
    """
    # Because the extensions are so easily represented as a string, this is one of the few classes
    # whose "managers" doesn't contain any special objects.
    
    def __init__(self, extension_list: list[str]) -> None:
        self.__extensions = set(extension_list)

        for ext in extension_list:
            if ext not in EXTENSIONS.values():
                raise ValueError(f"Error loading project: Project contains invalid Scratch extension {ext}.")
    
    @property
    def extensions(self) -> list[str]:
        """The list of this project's extensions, as a list of extension names."""
        return self.__extensions
    
    def add_extension(self, ext) -> None:
        """ Adds an extension to the project. The input can either be a value from EXTENSIONS, in 
            kurt3.extensions, or a native Scratch extension name (if you know them).
            Examples:   `extensions.add_extension(EXTENSIONS.TextToSpeech)`
                        `extensions.add_extension("pen")`, etc.
        """
        if ext in EXTENSIONS:
            self.__extensions.add(EXTENSIONS[ext])
        elif ext in EXTENSIONS.values():
            self.__extensions.add(ext)
        else:
            raise ValueError(f"Failed to add extension {ext} to project: extension does not exist.")
        
    def remove_extension(self, ext) -> None:
        """Removes a given extension from the project. The input can either be a value from EXTENSIONS, in 
            kurt3.extensions, or a native Scratch extension name (if you know them).
            Examples:   `extensions.remove_extension(EXTENSIONS.TextToSpeech)`,
                        `extensions.remove_extension("pen")`, etc.
        """

        if ext in EXTENSIONS and EXTENSIONS[ext] in self.__extensions:
            self.__extensions.remove(EXTENSIONS[ext])
        elif ext in EXTENSIONS.values() and ext in self.__extensions:
            self.__extensions.remove(ext)
        else:
            raise Warning(f"Warning: attempted to remove extension {ext}; extension was not already in the project.")
    
    def output(self) -> list[str]:
        return list(self.__extensions)