class Project:
    def __init__(self, repoName, name, branch, \
                 activeDateStart, activeDateEnd, lastChangeDate, \
                 description, \
                 imgNames, pLangs):
        self.repoName = repoName
        self.name = name
        self.branch = branch

        self.activeDateStart = activeDateStart
        self.activeDateEnd = activeDateEnd
        self.lastChangeDate = lastChangeDate

        self.description = description

        self.imgNames = imgNames
        self.pLangs = pLangs

def fetch_projects():
    projects = [
        Project("Adventure-Land-Bot", "Adventure Land Bot", "master",
            "2019-12-17", "2019-12-18", "2019-12-19",
            "My take on automating a party for the game Adventure Land",
            ["1-Game", "2-Game"],
            ["JS"]),
        Project("Console-VSRG-Trainer", "Console VSRG Trainer", "master",
            "2019-02-15", "2019-02-17", "2019-02-17",
            "My first take on a rhythm game trainer. Meaning it gives you a random combination of notes and waits for you to press the right keys.",
            ["1-Loading_Screen", "2-In_Game"],
            ["C#"])
    ]

    projects_to_js(projects)

def projects_to_js(projects):
    js = "let projects = {"
    for i in range(len(projects)):
        project = projects[i]
        js += project_to_js(project)

        if i != len(projects):
            js += ","
    js += "\n};\n"

    with open("js/projects.js", "w") as f:
        f.write(js)

def project_to_js(project):
    madeFor = "Hobby"
    if "Saxion" in project.repoName:
        madeFor = "Saxion"
    elif "ROC" in project.repoName:
        madeFor = "ROC"
    elif "Kunst-In-De-Etalage" in project.repoName:
        madeFor = "Internship"

    js = f"\n\t'{project.repoName}': new Project('{project.repoName}', '{project.name}', '{project.branch}', '{madeFor}'"
    js += f",\n\t\t'{project.activeDateStart}', '{project.activeDateEnd}', '{project.lastChangeDate}'"
    js += f",\n\t\t'{project.description}'"

    js += ",\n\t\t["
    for i in range(len(project.imgNames)):
        imgName = project.imgNames[i]

        if i != 0:
            js += ", "
        
        js += f"'Screenshots/{imgName}.png'"
    js += "]"

    js += ",\n\t\t["
    for i in range(len(project.pLangs)):
        pLang = project.pLangs[i]

        if i != 0:
            js += ", "
        
        js += f"'{pLang}'"
    js += "]"

    js += ")"
    return js

if __name__ == "__main__":
    fetch_projects()
