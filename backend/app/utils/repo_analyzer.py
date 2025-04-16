from glob import glob
from os import makedirs, system
from os.path import exists, isdir, join
from shutil import rmtree
from aiofiles import open

from .files.package_json_analyzer import analyze_package_json
from .files.pom_xml_analyzer import analyze_pom_xml
from .files.pyproject_toml_analyzer import analyze_pyproject_toml
from .files.requirements_txt_analyzer import analyze_requirements_txt
from .files.setup_cfg_analyzer import analyze_setup_cfg
from .files.setup_py_analyzer import analyze_setup_py

from app.http_session import get_session

pypi_files = ["pyproject.toml", "setup.cfg", "setup.py", "requirements.txt"]
npm_files = ["package.json"]
maven_files = ["pom.xml"]
all_files = set(pypi_files + npm_files + maven_files)


async def repo_analyzer(owner: str, name: str) -> dict[str, dict[str, dict | str]]:
    requirement_files: dict[str, dict[str, dict | str]] = {}
    repository_path = await download_repository(owner, name)
    requirement_file_names = await get_req_files_names(repository_path)
    for requirement_file_name in requirement_file_names:
        if "pom.xml" in requirement_file_name:
            requirement_files = await analyze_pom_xml(
                requirement_files, repository_path, requirement_file_name
            )
        elif "package.json" in requirement_file_name:
            requirement_files = await analyze_package_json(
                requirement_files, repository_path, requirement_file_name
            )
        elif "pyproject.toml" in requirement_file_name:
            requirement_files = await analyze_pyproject_toml(
                requirement_files, repository_path, requirement_file_name
            )
        elif "setup.cfg" in requirement_file_name:
            requirement_files = await analyze_setup_cfg(
                requirement_files, repository_path, requirement_file_name
            )
        elif "setup.py" in requirement_file_name:
            requirement_files = await analyze_setup_py(
                requirement_files, repository_path, requirement_file_name
            )
        elif "requirements.txt" in requirement_file_name:
            requirement_files = await analyze_requirements_txt(
                requirement_files, repository_path, requirement_file_name
            )
    system("rm -rf " + repository_path)
    return requirement_files


async def download_repository(owner: str, name: str) -> str:
    repository_path = f"repositories/{name}"
    if exists(repository_path):
        rmtree(repository_path)
    makedirs(repository_path)
    session = await get_session()
    url = f"https://api.github.com/repos/{owner}/{name}/contents"
    async with session.get(url) as resp:
        if resp.status != 200:
            print(f"Error fetching contents of {owner}/{name}")
            return repository_path
        contents = await resp.json()
    for item in contents:
        if item["type"] == "file" and item["name"] in all_files:
            raw_url = item["download_url"]
            async with session.get(raw_url) as file_resp:
                if file_resp.status == 200:
                    file_content = await file_resp.text()
                    filepath = join(repository_path, item["name"])
                    async with open(filepath, "w") as f:
                            await f.write(file_content)
    return repository_path


async def get_req_files_names(directory_path: str) -> list[str]:
    requirement_files = []
    paths = glob(directory_path + "/**", recursive=True)
    for _path in paths:
        if not isdir(_path) and await is_req_file(_path):
            requirement_files.append(
                _path.replace(directory_path, "").replace(directory_path, "")
            )
    return requirement_files


async def is_req_file(requirement_file_name: str) -> bool:
    if any(extension in requirement_file_name for extension in pypi_files):
        return True
    if any(extension in requirement_file_name for extension in npm_files):
        return True
    if any(extension in requirement_file_name for extension in maven_files):
        return True
    return False
