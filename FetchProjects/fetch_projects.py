import os
import re
import requests
import subprocess
from bs4 import BeautifulSoup

class Project:
    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.name = ""
        self.branch = ""

        self.active_date_start = ""
        self.active_date_end = ""
        self.last_change_date = ""

        self.description = ""

        self.img_filenames = []
        self.p_langs = []

def fetch_projects():
    projects = repos_to_projects()
    js = projects_to_js(projects)
    with open("../js/projects.js", "w") as f:
        f.write(js)
    
    print("Done!")

def repos_to_projects():
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

            print(f"=== {repo_name} ===")
            project = Project(repo_name)
            set_data_from_github_page(project, github_page)
            set_data_from_local_clone(project, repo_path)

            projects.append(project)

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
    except Exception as e:
        print(e)

    return github_page

def set_data_from_github_page(project, github_page):
    soup = BeautifulSoup(github_page, 'html.parser')
    
    html_langs_header = soup.find('h2', string='Languages')
    if not html_langs_header:
        print("No 'Languages' header in the HTML.")
        return
    
    html_langs = html_langs_header.find_next('ul')
    for html_lang in html_langs.find_all('li'):
        lang_percentage = float(html_lang.find('span', string=lambda t: t and '%' in t).text.strip('%'))
        if lang_percentage < 10:
            continue

        lang_name = html_lang.find_next('span').text.strip()
        project.p_langs.append(lang_name)
    
    if len(project.p_langs) == 0:
        print("Could not extract languages from the HTML.")

def set_data_from_local_clone(project, repo_path):
    set_screenshot_filenames(project, repo_path)
    set_main_branch_name(project, repo_path)
    set_data_from_readme(project, repo_path)

def set_screenshot_filenames(project, repo_path):
    screenshots_path = os.path.join(repo_path, "Screenshots")
    if not os.path.exists(screenshots_path):
        print("No 'Screenshots' directory.")
        return
    
    for filename in os.listdir(screenshots_path):
        if filename.lower().endswith('.png'):
            project.img_filenames.append(filename)
    
    if len(project.img_filenames) == 0:
        print("No PNGs in the 'Screenshots' directory.")

def set_main_branch_name(project, repo_path):
    git_dir_path = os.path.join(repo_path, ".git")
    try:
        remote_show_proc = subprocess.run(
            ['git', '--git-dir', git_dir_path, 'remote', 'show', 'origin'],
            capture_output=True,
            text=True,
            check=True)
        
        remote_show_output = remote_show_proc.stdout
        match = re.search(r'^\s*HEAD branch:\s*(\S+)', remote_show_output, re.MULTILINE)
        
        if not match:
            print("Could not extract the branch name.")
            return

        project.branch = match.group(1)
    except Exception as e:
        print(e)

def set_data_from_readme(project, repo_path):
    readme_path = os.path.join(repo_path, "README.md")
    if not os.path.exists(readme_path):
        print("No 'README.md' file.")
        return
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read().replace(("\r\n"), "\n").replace("\n\r", "\n")
    
    project.name = readme.split("\n")[0].replace("#", "").strip()

    description = readme.split("\n")[1].strip()
    if not any(description.endswith(term) for term in ['.', '!', '?']):
        last_terminator = max(description.rfind('.'), description.rfind('!'), description.rfind('?'))
        if last_terminator != -1:
            description = description[:last_terminator + 1]
    
    # Change markdown link syntax `[text](url)`` into just the text
    description = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', description)

    project.description = description

    active_date_range = readme.split("**Active Development:**")[1].split("<br>")[0].strip()
    project.active_date_start, project.active_date_end = active_date_range.split(" - ")

    project.last_change_date = readme.split("**Last Change:**")[1].split("<br>")[0].strip()

def projects_to_js(projects):
    js = "let projects = {"
    for i in range(len(projects)):
        project = projects[i]
        js += project_to_js(project)

        if i != len(projects):
            js += ","
    js += "\n};\n"
    return js

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
    for i in range(len(project.img_filenames)):
        img_name = project.img_filenames[i]

        if i != 0:
            js += ", "
        
        js += f"'Screenshots/{img_name}'"
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
