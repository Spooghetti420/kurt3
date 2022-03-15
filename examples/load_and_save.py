def main():
    from kurt3.project import Project

    with Project("projects/src/Blank Project.sb3") as project: 
        project.save("projects/out/Test Saving.sb3")

if __name__ == "__main__":
    main()