from kurt3.blocks.motion import *
from kurt3.project import Project


def main():
    with Project("../assets/Blank Project.sb3") as project:
        sprite = project.get_sprite_by_name("Sprite1")
        sprite.add_block(MoveSteps(project, 10))
        sprite.add_block(TurnRight(project, 90))
        sprite.add_block(TurnLeft(project, 90))
        sprite.add_block(GoToXY(project, 10, 10))
        sprite.add_block(GlideSecsToMenu(project, 1, "_mouse_"))
        sprite.add_block(GlideSecsToXY(project, 10, 50, 50))
        sprite.add_block(PointInDirection(project, 90))
        sprite.add_block(ChangeXBy(project, 10))
        sprite.add_block(ChangeYBy(project, 10))
        sprite.add_block(SetX(project, 10))
        sprite.add_block(SetY(project, 10))
        sprite.add_block(IfOnEdgeBounce(project))
        sprite.add_block(SetRotationStyle(project, "don't rotate"))
        sprite.add_block(XPosition(project))
        sprite.add_block(YPosition(project))
        sprite.add_block(Direction(project))
        project.save("../out/Motion Blocks.sb3")

if __name__ == "__main__":
    main()