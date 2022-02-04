class MetaDataManager:
    def __init__(self, meta_json) -> None:
        """
        A class to manage project metadata. There are only three properties,
        `semver`, `vm`, and `user_agent`.
        """
        self.__semver = meta_json["semver"]
        self.__vm = meta_json["vm"]
        self.__user_agent = meta_json["agent"]

    @property
    def semver(self) -> str:
        """
        The semantic version of the project when it was exported.
        A semver is the familiar format MAJOR.minor.patch, e.g. 1.7.10,
        or in the case of a Scratch 3 project, almost invariably 3.0.0.
        Any semver with a major version of 3 is compatible with Scrath 3.
        """
        return self.__semver
    
    @property
    def vm(self) -> str:
        """
        The version of the Scratch VM that this project was exported from. Critical to the process of loading the
        project in Scratch.
        """
        return self.__vm

    @property
    def user_agent(self):
        """
        The user agent detected when the project was exported. Is not relevantto loading the project and can be spoofed.
        """
        return self.__user_agent
    
    @user_agent.setter
    def set_user_agent(self, value):
        if type(value) is not str:
            raise TypeError(f"User agent must be a string, but {value} of type {type(value)} was received.")

    # Re-serialize the metadata
    def output(self):
        return {
            "semver": self.__semver,
            "vm": self.__vm,
            "agent": self.__user_agent
        }