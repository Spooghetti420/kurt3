from kurt3.project import Project

def main():
    with Project("projects/src/Blank Project.sb3") as project:
        sprite1 = project.get_sprite_by_name("Sprite1")
        project.add_costume(sprite1, "assets/Bread.svg", "Bread1")
        project.add_costume(sprite1, "assets/Bread.svg", "Bread2")
        project.add_sound(sprite1, "assets/A Bass.wav", "Bass1")
        
        project.save("projects/out/File Adding Test.sb3")

if __name__ == "__main__":
    main()