from kurt3.blocks.looks import *
from kurt3.project import Project


def main():
    with Project("../assets/Blank Project.sb3") as project:
        sprite = project.get_sprite_by_name("Sprite1")
        sprite.add_block(SayForSecs(project, 2, "Sample Text 1"))
        sprite.add_block(Say(project, "Sample Text 2"))
        sprite.add_block(ThinkForSecs(project, 2, "Sample Text 3"))
        sprite.add_block(Think(project, "Sample Text 4"))
        sprite.add_block(SwitchCostumeTo(project, "costume1"))
        sprite.add_block(NextCostume(project))
        sprite.add_block(SwitchBackdropTo(project, "backdrop1"))
        sprite.add_block(ChangeSizeBy(project, 50))
        sprite.add_block(SetSizeTo(project, 100))
        sprite.add_block(ChangeEffectBy(project, "COLOR", -50))
        sprite.add_block(SetEffectTo(project, "COLOR",  50))
        sprite.add_block(ClearGraphicsEffects(project))
        sprite.add_block(Show(project))
        sprite.add_block(Hide(project))
        sprite.add_block(GoToFrontBack(project, "back"))
        sprite.add_block(GoForwardBackwardLayers(project, "forward", 3))
        sprite.add_block(CostumeNumberName(project, "number"))
        sprite.add_block(BackdropNumberName(project, "name"))
        sprite.add_block(Size(project))
        project.save("../out/Looks Blocks.sb3")

if __name__ == "__main__":
    main()