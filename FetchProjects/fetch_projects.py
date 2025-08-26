import os
import requests

class Project:
    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.name = ""
        self.branch = ""

        self.active_date_start = ""
        self.active_date_end = ""
        self.last_change_date = ""

        self.description = ""

        self.img_names = []
        self.p_langs = []

def fetch_projects():
    projects = projects_from_local_repos()
    projects_to_js(projects)

def projects_from_local_repos():
    projects = []

    repos_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for repo_name in os.listdir(repos_path):
        repo_path = os.path.join(repos_path, repo_name)
        if os.path.isdir(repo_path):
            if not os.path.exists(os.path.join(repo_path, ".git")):
                continue

            github_page = get_github_page(repo_name)
            # Not a GitHub repo or not public
            if github_page == None:
                continue

            project = Project(repo_name)
            get_data_from_github_page(project, github_page)
            get_data_from_readme(project, repo_path)

            projects.append(project)

            break

    return projects

def get_github_page(repo_name):
    github_page = None

    url = f"https://github.com/Emanuel-de-Jong/{repo_name}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            if ">Public</span>" in html:
                github_page = html
    except Exception as ex:
        print(ex)

    return github_page

def get_data_from_github_page(project, github_page):
    html_langs = github_page.split(">Languages</h2>")[1].split("</turbo-frame>")[0]
    html_langs = html_langs.strip().replace("\n", "").replace("  ", "").replace("\t", "")

    for html_lang in html_langs.split("<li"):
        lang_percentage = html_lang.split("%</span")[0].split("<span>")[-1]
        print(lang_percentage)

def get_data_from_readme(project, repo_path):
    pass

def projects_to_js(projects):
    js = "let projects = {"
    for i in range(len(projects)):
        project = projects[i]
        js += project_to_js(project)

        if i != len(projects):
            js += ","
    js += "\n};\n"

    with open("../Website/js/projects.js", "w") as f:
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
