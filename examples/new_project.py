from kurt3.project import Project


with Project.new_project() as project:
    project.save("../out/New Project.sb3")