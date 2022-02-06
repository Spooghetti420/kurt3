from __future__ import annotations
import os
import traceback
import zipfile
import tempfile
import json as JSON
from shutil import rmtree
from kurt3.extensions import ExtensionManager
from kurt3.metadata import MetadataManager
from kurt3.monitor import MonitorManager
from kurt3.target import TargetManager

class Project:
    def __init__(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Project could not be found at {file_path}.")

        self.__filepath = file_path
        self.__filename = os.path.split(file_path)[1]
        self.__tmp = tempfile.gettempdir()
        self.__tmp_dir_name = os.path.join(self.__tmp, self.__filename)

    def __enter__(self) -> Project:
        with zipfile.ZipFile(self.__filepath, "r") as zip_ref:
            zip_ref.extractall(self.__tmp_dir_name)
        
        self.__json = ProjectJSON(os.path.join(self.__tmp_dir_name, "project.json"))
        return self

    
    def __exit__(self, exception_type, exception_value, tb):
        if exception_type is not None:
            traceback.print_exception(exception_type, exception_value, tb)

        # Removes the temporary working directory once the project is finished with
        rmtree(self.__tmp_dir_name)
        return True

    @property
    def targets(self):
        return self.__json.targets

    @property
    def monitors(self):
        return self.__json.monitors

    @property
    def extensions(self):
        return self.__json.extensions

    @property
    def metadata(self):
        return self.__json.metadata
        
    def save(self, file_path: str = "project.sb3"):
        """
        Output the project as a file, with the optional `file_path` attribute to specify where to save to.
        The default filename is `project.sb3`.
        """

        if type(file_path) is not str:
            raise TypeError(f"File output name must be a string, but {file_path} of type {type(file_path)} was received.")
        
        directory_path = os.path.split(file_path)[0] 
        if directory_path != "" and not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory {directory_path} where the project was saved could not be found.")

        with open(os.path.join(self.__tmp_dir_name, "project.json"), mode="w") as project_file:
            project_file.write(JSON.dumps(self.__json.output()))

        with zipfile.ZipFile(file_path, "w") as zip_ref:
            for file in os.listdir(self.__tmp_dir_name):
                zip_ref.write(os.path.join(self.__tmp_dir_name, file), file)

class ProjectJSON:
    """
    Represents a Scratch project's `project.json` file. Allows access to all
    of the project's inherent structural data, such as sprites, and their
    costumes, sounds, scripts, etc.
    """

    def __init__(self, project_json_file: str) -> None:
        """
        Initialize a project using the its filename.
        """
        self.__json = ""
        with open(project_json_file) as project_json:
            self.__json = project_json.read()

        parsed_json: dict = JSON.loads(self.__json)
        
        self.__targets = TargetManager(parsed_json["targets"])
        self.__monitors = MonitorManager(parsed_json["monitors"])
        self.__extensions = ExtensionManager(parsed_json["extensions"])
        self.__metadata = MetadataManager(parsed_json["meta"])

    @property
    def targets(self) -> TargetManager:
        """
        The `Target`s that belong to this project, i.e. all sprites and the stage.
        """
        return self.__targets
    
    @property
    def monitors(self) -> MonitorManager:
        """
        The variable and list monitors on display on this project.
        """
        return self.__monitors
    
    @property
    def extensions(self) -> ExtensionManager:
        """
        The list of extensions enabled on this project.
        """
        return self.__extensions
    
    @property
    def metadata(self) -> MetadataManager:
        """
        The metadata associated with this project.
        """
        return self.__metadata
    
    @property
    def stage(self):
        return self.targets.get_stage()

    def output(self) -> dict:
        """ Returns a new project.json-compatible output dictionary from the project data.
            This contains the properties of a Scratch project, namely `targets`, `monitors`,
            `extensions`, and `meta`.
        """

        return {
            "targets": self.__targets.output(),
            "monitors": self.__monitors.output(),
            "extensions": self.__extensions.output(),
            "meta": self.__metadata.output()
        }