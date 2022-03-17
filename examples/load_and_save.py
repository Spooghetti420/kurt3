def main():
    from kurt3.project import Project

    with Project("../assets/Blank Project.sb3") as project: 
        project.save("../out/Test Saving.sb3")

if __name__ == "__main__":
    main()