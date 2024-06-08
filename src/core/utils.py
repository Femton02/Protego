import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#
import json

def read_file(file_path: str) -> str:
    """Reads the contents of a file and returns it as a string.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The contents of the file.
    """
    with open(file_path, "r") as file:
        return file.read()
    

def get_js_files(
        project_path: str,
) -> list[str]:
    """Get the paths of all JavaScript files in a project.

    Args:
        project_path (str): The path to the project.

    Returns:
        list[str]: A list of paths to JavaScript files in the project.
    """
    if not os.path.exists(project_path):
        raise Exception(f"Project path: {project_path} does not exist.")
    
    print(f"Getting JavaScript files in project: {project_path}")
    target_files = []
    if os.path.isfile(project_path):
        if any(project_path.endswith(extension) for extension in js_supported_extensions):
            target_files.append(project_path)

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if any(file.endswith(extension) for extension in js_supported_extensions):
                target_files.append(os.path.join(root, file))

    return target_files


def read_json_file(file_path: str) -> dict:
    """Reads the contents of a JSON file and returns it as a dictionary.

    Args:
        file_path (str): The path to the JSON file to read.

    Returns:
        dict: The contents of the JSON file.
    """
    with open(file_path, "r") as file:
        return json.load(file)