class Project:
    def __init__(self, repo_name, name, branch, \
                 active_date_start, active_date_end, last_change_date, \
                 description, \
                 img_names, p_langs):
        self.repo_name = repo_name
        self.name = name
        self.branch = branch

        self.active_date_start = active_date_start
        self.active_date_end = active_date_end
        self.last_change_date = last_change_date

        self.description = description

        self.img_names = img_names
        self.p_langs = p_langs

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
    made_for = "Hobby"
    if "Saxion" in project.repo_name:
        made_for = "Saxion"
    elif "ROC" in project.repo_name:
        made_for = "ROC"
    elif "Kunst-In-De-Etalage" in project.repo_name:
        made_for = "Internship"

    js = f"\n\t'{project.repo_name}': new Project('{project.repo_name}', '{project.name}', '{project.branch}', '{made_for}'"
    js += f",\n\t\t'{project.active_date_start}', '{project.active_date_end}', '{project.last_change_date}'"
    js += f",\n\t\t'{project.description}'"

    js += ",\n\t\t["
    for i in range(len(project.img_names)):
        img_name = project.img_names[i]

        if i != 0:
            js += ", "
        
        js += f"'Screenshots/{img_name}.png'"
    js += "]"

    js += ",\n\t\t["
    for i in range(len(project.p_langs)):
        p_lang = project.p_langs[i]

        if i != 0:
            js += ", "
        
        js += f"'{p_lang}'"
    js += "]"

    js += ")"
    return js

if __name__ == "__main__":
    fetch_projects()
