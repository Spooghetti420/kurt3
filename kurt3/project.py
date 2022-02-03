import json
from kurt3.extensions import ExtensionManager
from kurt3.metadata import MetaDataManager
from kurt3.monitor import MonitorManager
from kurt3.target import TargetManager


class Project:

    def __init__(self, json_data):
        self.__json = json_data
        parsed_json: dict = json.loads(json_data)
        
        self.targets = TargetManager(parsed_json["targets"])
        self.monitors = MonitorManager(parsed_json["monitors"])
        self.extensions = ExtensionManager(parsed_json["extensions"])
        self.metadata = MetaDataManager(parsed_json["meta"])

    def output(self):
        return {
            "targets": self.targets.output(),
            "monitors": self.monitors.output(),
            "extensions": self.extensions.output(),
            "meta": self.metadata.output()
        }