from kurt3.project import Project


with Project("../assets/Blank Project.sb3") as project:
    n = project.create_sprite("Sprite2")
    project.save("../out/Add Sprite.sb3")