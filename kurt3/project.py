import json
from kurt3.extensions import ExtensionManager
from kurt3.metadata import MetaDataManager
from kurt3.monitor import MonitorManager
from kurt3.target import TargetManager


class Project:
    """
    Represents a Scratch project's `project.json` file. Allows access to all
    of the project's inherent structural data, such as sprites, and their
    costumes, sounds, scripts, etc.
    """

    def __init__(self, json_data: str) -> None:
        self.__json = json_data
        parsed_json: dict = json.loads(json_data)
        
        self.targets = TargetManager(parsed_json["targets"])
        self.monitors = MonitorManager(parsed_json["monitors"])
        self.extensions = ExtensionManager(parsed_json["extensions"])
        self.metadata = MetaDataManager(parsed_json["meta"])
    
    @property
    def stage(self):
        return self.targets.get_stage()

    def output(self) -> dict:
        """ Returns a new project.json-compatible output dictionary from the project data.
            This contains the properties of a Scratch project, namely `targets`, `monitors`,
            `extensions`, and `meta`.
        """

        return {
            "targets": self.targets.output(),
            "monitors": self.monitors.output(),
            "extensions": self.extensions.output(),
            "meta": self.metadata.output()
        }