import os
import re
import sys
import logging
import requests
import subprocess
from bs4 import BeautifulSoup

class Project:
    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.name = ""
        self.branch = ""
        self.made_for = ""

        self.active_date_start = ""
        self.active_date_end = ""
        self.last_change_date = ""

        self.description = ""

        self.img_paths = []
        self.highlights = []
        self.p_langs = []

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("log.log", encoding="utf-8", mode="a")
    file_handler.setFormatter(logging.Formatter(
        "[{asctime}][{levelname}]: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{"
    ))

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(
        "[{levelname}]: {message}",
        style="{"
    ))

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

logger = setup_logger()

def fetch_projects():
    logger.info("Fetching projects...")

    projects = repos_to_projects()
    js = projects_to_js(projects)
    with open("../js/projects.js", "w") as f:
        f.write(js)
    
    logger.info("Done!")

def repos_to_projects():
    projects = []

    repos_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    repo_names = sorted(os.listdir(repos_path))
    for repo_name in repo_names:
        repo_path = os.path.join(repos_path, repo_name)
        if os.path.isdir(repo_path):
            if not os.path.exists(os.path.join(repo_path, ".git")):
                continue

            github_page = get_github_page(repo_name)
            # Not a GitHub repo or not public.
            if github_page == None:
                continue

            logger.info(f"=== {repo_name} ===")
            project = Project(repo_name)

            project.made_for = "Hobby"
            if "Saxion" in repo_name:
                project.made_for = "Saxion"
            elif "ROC" in repo_name:
                project.made_for = "ROC"

            if "Kunst-In-De-Etalage" in repo_name:
                project.made_for = "Internship"
                project.p_langs = ["PHP", "JavaScript", "HTML", "CSS"]
            elif "Portfolio-2019" in repo_name:
                project.p_langs = ["HTML", "CSS"]

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
        logger.error(e, exc_info=True)

    return github_page

def set_data_from_github_page(project, github_page):
    soup = BeautifulSoup(github_page, 'html.parser')

    if len(project.p_langs) == 0:
        html_langs_header = soup.find('h2', string='Languages')
        if not html_langs_header:
            logger.warning("No 'Languages' header in the HTML.")
            return
        
        html_langs = html_langs_header.find_next('ul')
        for html_lang in html_langs.find_all('li'):
            html_percentage = html_lang.find('span', string=lambda t: t and '%' in t)
            lang_percentage = float(html_percentage.text.strip('%').strip())
            if lang_percentage < 1:
                continue

            lang_name = html_lang.find('span', class_='color-fg-default').text.strip().replace(" ", "-")
            if lang_name == "Other":
                continue
            
            project.p_langs.append(lang_name)
        
        if len(project.p_langs) == 0:
            logger.warning("Could not extract languages from the HTML.")

def set_data_from_local_clone(project, repo_path):
    set_screenshot_paths(project, repo_path)
    set_main_branch_name(project, repo_path)
    set_data_from_readme(project, repo_path)

def set_screenshot_paths(project, repo_path):
    screenshots_path = None
    for dir in ["Screenshots", "screenshots"]:
        path = os.path.join(repo_path, dir)
        if os.path.exists(path):
            screenshots_path = path
            break

    if not screenshots_path:
        # logger.warning("No 'Screenshots' directory.")
        return
    
    dir = os.path.basename(screenshots_path)
    filenames = sorted(os.listdir(screenshots_path))
    for filename in filenames:
        if filename.lower().endswith(".png"):
            project.img_paths.append(f"{dir}/{filename}")
    
    # if len(project.img_paths) == 0:
    #     logger.warning("No PNGs in the 'Screenshots' directory.")

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
            logger.warning("Could not extract the branch name.")
            return

        project.branch = match.group(1)
    except Exception as e:
        logger.error(e, exc_info=True)

def set_data_from_readme(project, repo_path):
    readme_path = os.path.join(repo_path, "README.md")
    if not os.path.exists(readme_path):
        logger.warning("No 'README.md' file.")
        return
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read().replace(("\r\n"), "\n").replace("\n\r", "\n")
    
    name = readme.split("\n")[0].replace("#", "").strip()
    name = name.replace("'", "")
    project.name = name

    description_line_index = 1
    if (project.made_for == "Saxion"):
        description_line_index = 3

    description = ""
    lines = readme.split("\n")
    while description_line_index < len(lines):
        line = lines[description_line_index].strip()
        if line and not line.startswith(">"):
            description = line
            break
        
        description_line_index += 1

    description = description.strip().replace("`", "")
    
    # Change markdown link syntax `[text](url)`` into just the text.
    description = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', description)

    # Max 220 characters.
    description = description[:220]

    if not any(description.endswith(term) for term in ['.', '!', '?']):
        last_terminator = max(description.rfind('.'), description.rfind('!'), description.rfind('?'))
        if last_terminator != -1:
            description = description[:last_terminator + 1]

    project.description = description

    active_date_range = get_readme_field_values(readme, "Active Development")
    project.active_date_start, project.active_date_end = active_date_range.split(" - ")

    project.last_change_date = get_readme_field_values(readme, "Last Change")
    
    highlights_str = get_readme_field_values(readme, "Highlights")
    if highlights_str != None:
        highlights = highlights_str.split(", ")
        project.highlights = [highlight.replace(" ", "-") for highlight in highlights]

def get_readme_field_values(readme, field_name):
    field_split = readme.split(f"**{field_name}:**")
    if len(field_split) < 2:
        return None
    
    return field_split[1].split("<br>")[0].strip()

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
    js = f"\n\t'{project.repo_name}': new Project('{project.repo_name}', '{project.name}', '{project.branch}', '{project.made_for}'"
    js += f",\n\t\t'{project.active_date_start}', '{project.active_date_end}', '{project.last_change_date}'"
    js += f",\n\t\t`{project.description}`"

    js += list_to_js(project.img_paths)
    js += list_to_js(project.highlights)
    js += list_to_js(project.p_langs)

    js += ")"
    return js

def list_to_js(l):
    js = ",\n\t\t["
    for i in range(len(l)):
        if i != 0:
            js += ", "
        
        js += f"'{l[i]}'"
    js += "]"
    return js

if __name__ == "__main__":
    try:
        fetch_projects()
    except Exception as e:
        logger.error(e, exc_info=True)
        sys.exit(1)
