from __future__ import annotations
import hashlib
import os
import random
import shutil
import traceback
import zipfile
import tempfile
import json as JSON
from kurt3.asset import AssetData
from kurt3.extensions import ExtensionManager
from kurt3.metadata import MetadataManager
from kurt3.monitor import MonitorManager
from kurt3.target import Sprite, Target, TargetManager
from kurt3.variable import Variable

class Project:
    def __init__(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Project could not be found at {file_path}.")

        self.__filepath = file_path
        self.__filename = os.path.split(file_path)[1]
        self.__tmp = tempfile.gettempdir()
        self.__tmp_dir_name = os.path.join(self.__tmp, self.__filename)

        self.__json = ""

        self.__targets: TargetManager = None
        self.__monitors: MonitorManager = None
        self.__extensions: ExtensionManager = None
        self.__metadata: MetadataManager = None

        self._assets = dict() # List of newly added assets to avoid re-hashing files

    def __enter__(self) -> Project:
        with zipfile.ZipFile(self.__filepath, "r") as zip_ref:
            zip_ref.extractall(self.__tmp_dir_name)

        
        with open(os.path.join(self.__tmp_dir_name, "project.json")) as project_json:
            self.__json = project_json.read()

        parsed_json: dict = JSON.loads(self.__json)
        
        self.__targets = TargetManager(parsed_json["targets"])
        self.__monitors = MonitorManager(parsed_json["monitors"])
        self.__extensions = ExtensionManager(parsed_json["extensions"])
        self.__metadata = MetadataManager(parsed_json["meta"])
        return self

    
    def __exit__(self, exception_type, exception_value, tb):
        if exception_type is not None:
            traceback.print_exception(exception_type, exception_value, tb)

        # Removes the temporary working directory once the project is finished with
        shutil.rmtree(self.__tmp_dir_name)
        return True

    @staticmethod
    def new_project() -> Project:
        return Project("../assets/Blank Project.sb3")

    def _add_asset(self, file_path) -> None:
        if file_path in self._assets:
            return

        self._check_file_path(file_path)

        with open(file_path, mode="rb") as asset:
            md5_hash = hashlib.md5(asset.read()).hexdigest()
            extension = os.path.splitext(file_path)[1]
            self._assets[file_path] = AssetData(md5_hash, extension)

    def generate_id(self, l = 20) -> str:
        valid_characters = "!#$%()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        existing_ids = self._get_ids()
        # Generate IDs until a unique one is found (very likely the first attempt) 
        while (uuid := "".join([random.choice(valid_characters) for i in range(l)])) in existing_ids:
            pass
        return uuid

    def _get_ids(self) -> list[str]:
        ids = set()
        for t in self.targets:
            for m in t.blocks._items + t.broadcasts._items + t.variables._items + t.lists._items:
                ids.add(m._id)
        return ids

    def _get_highest_layer(self) -> int:
        return max([t.layer for t in self.targets])

    @staticmethod
    def _check_file_path(file_path) -> None:
        if type(file_path) is not str:
            raise TypeError(f"File name must be a string, but {file_path} of type {type(file_path)} was received.")
        
        directory_path = os.path.split(file_path)[0] 
        if directory_path != "" and not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)

    @property
    def targets(self):
        return self.__targets

    @property
    def monitors(self):
        return self.__monitors

    @property
    def extensions(self):
        return self.__extensions

    @property
    def metadata(self):
        return self.__metadata

    @property
    def stage(self):
        return self.targets.get_stage()

    def get_variables_by_name(self, name) -> list[Variable]:
        """
        Get any variables that correspond to the given name.
        Any global variable will only be returned as one instance,
        belonging to the Stage; local variables mean that the
        return value is a list, where multiple duplicate local variables
        can each appear in the list.
        """

        output = []
        for target in self.__targets.as_list():
            if (vars := target.variables.by_name(name)):
                output.extend(vars)
        return output

    def get_sprite_by_name(self, name) -> Sprite:
        """
        Returns the sprite, if any, that corresponds to the given
        `name`, else raises an error.
        """
        return self.__targets.get_sprite_by_name(name)

    def _add_asset_check(self, param_name: str, oftype: type, value):
        if type(value) is not oftype:
            raise TypeError(f"{param_name} name must be a {str(oftype)}, but {value} of type {type(value)} was received.")
        
    def add_costume(self, target: Target, file_path: str, name: str):
        self._add_asset_check("File path", str, file_path)
        self._add_asset_check("Costume name", str, name)

        if bool([c for c in target.costumes.costumes if c.name == name]):
            raise ValueError(f"The chosen costume name ({name}) already exists on this Target. Please choose a different one.")
        
        self._check_file_path(file_path)
        
        if file_path not in self._assets:
            self._add_asset(file_path)

        md5, extension = self._assets[file_path]
        target.costumes._add(md5, name, extension)

    def add_sound(self, target: Target, file_path: str, name: str):
        self._add_asset_check("File path", str, file_path)
        self._add_asset_check("Sound name", str, name)
      
        self._check_file_path(file_path)
        
        if file_path not in self._assets:
            self._add_asset(file_path)
        
        if bool([s for s in target.sounds.sounds if s.name == name]):
            raise ValueError(f"The chosen sound name ({name}) already exists on this Target. Please choose a different one.")

        md5, extension = self._assets[file_path]
        target.sounds._add(md5, extension, name)

    def create_sprite(self, name: str):
        """
        Create and return a `Sprite` that is added to the project.
        """
        s = Sprite(name=name, layerOrder=self._get_highest_layer()+1)
        self.targets._add_sprite(s)
        return s

    def _run_presave_compatibility_check(self):
        """
        Ensure that the project is correctly configured so as to guarantee importability
        in Scratch.
        """
        for target in self.__targets:
            # All sprites require at least one costume for the project to be valid.
            if len(target.costumes) == 0:
                # Add the "cat" costume to costumeless sprites
                self.add_costume(target, "../assets/cat1.svg", "costume1")
        
    def save(self, file_path: str = "project.sb3"):
        """
        Output the project as a file, with the optional `file_path` attribute to specify where to save to.
        The default filename is `project.sb3`.
        """
        if not os.path.exists(self.__tmp_dir_name):
            raise IOError("Project file already closed; please save the project inside the with-block.")

        self._check_file_path(file_path)
        self._run_presave_compatibility_check()

        for file, (md5_name, extension) in self._assets.items():
            shutil.copy(file, f"{os.path.join(self.__tmp_dir_name, md5_name + extension)}")

        with open(os.path.join(self.__tmp_dir_name, "project.json"), mode="w") as project_file:
            project_file.write(JSON.dumps(self.output()))

        with zipfile.ZipFile(file_path, "w") as zip_ref:
            for file in os.listdir(self.__tmp_dir_name):
                zip_ref.write(os.path.join(self.__tmp_dir_name, file), file)

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