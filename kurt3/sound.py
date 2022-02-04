from kurt3.asset import Asset


class SoundManager:
    def __init__(self, sound_list: list[dict]) -> None:
        self.__sounds = [Sound(s) for s in sound_list]
    
    def output(self):
        return [s.output() for s in self.__sounds]

    @property
    def sounds(self):
        """
        The sounds that belong to this target.
        """
        return self.__sounds
    
class Sound(Asset):
    def __init__(self, values: dict) -> None:
        super().__init__(values)
        self.__format = values["format"]
        self.__rate = values["rate"]
        self.__sample_count = values["sampleCount"]
        
    @property
    def sample_count(self) -> int:
        """
        The number of distinct audio samples in this sound. Together with the sound's frequency, this allows
        the sound's length to be determined.
        """
        return self.__sample_count
    
    @property
    def sample_rate(self) -> int:
        """
        The sample rate of the sound file, represented in Hz. Together with the sound's sample count, this allows
        the sound's length to be determined.
        """
        return self.__rate
    
    @sample_rate.setter
    def set_sample_rate(self, value):
        if type(value) is not int:
            raise TypeError(f"Sound's sample rate must be an integer, but {value} of type {type(value)} was received.")

        if 0 < value <= 192000:
            self.__rate = value
        else:
            raise ValueError(f"Sample rate ({value} must be between 1 and 192000Hz inclusive.")

    # Question: how is "format" different from "dataFormat"?

    def output(self):
        return super().output() | {
            "format": self.__format,
            "rate": self.__rate,
            "sampleCount": self.__sample_count,
        }