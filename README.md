# kurt3 (Scratch project v3 API)
This is a Python library that can be used to programatically modify `.sb3` files.
It supports adding assets (costumes and sounds) to existing sprites, modifying various project data, and
(eventually) will support adding blocks. For those unfamilair with Scratch, you can learn more about it at [scratch.mit.edu](scratch.mit.edu).

## Usage examples
You can use the `with` keyword to "open" the project and use the `Project`'s context manager and consequently access methods to modify the project.
```
from kurt3.project import Project

with Project("path/to/project/Blank Project.sb3") as project:
    sprite1 = project.get_sprite_by_name("Sprite1")
    project.add_costume(sprite1, "Bread.svg", "Bread1")
    project.add_costume(sprite1, "assets/Bread.svg", "Bread2")
    project.add_sound(sprite1, "assets/A Bass.wav", "Bass1")

    project.save("output/file/path/File Adding Test.sb3")
```
For further examples and usages, see the `examples` folder.

## Inspiration
This project is invigorated by the former "kurt" project, which offered the same functionality to users during the Scratch 2 era.
With the advent of Scratch 3 came a new file format, which deprecated the old one, and the kurt API with it. As such, I was inspired to develop a successor so that similarly innovative applications could be generated programatically.

## File format information
Scratch projects consist of a `zip` file containing all of its assets, whose filenames correspond to the MD5 hash of their file contents.
The most critical file to the structure of the project is the `project.json` file, which holds within all the data concerning the project, and through the modification of which the project can be externally altered.
In it are all kinds of structures, at the top level the "targets" (sprites + the stage), "monitors" (the variable/list displays),
"extensions" (what extensions are enabled in the project), and "metadata", which effectively captures details about the project creator and the version of Scratch it was made in. The API exposes object-oriented abstractions of this JSON data, which allows one to robustly edit a Scratch project.