import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#
import re
import json
import uuid

jsons_files_path = os.path.join(protego_workspace_dir, "../bearer/internal/classification/db/recipes")

def read_json_file(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return json.load(file)

# Each json file contains the following structure:
# {
#   "metadata": { "version": "1.0" },
#   "name": "Envoy",
#   "type": "external_service",
#   "urls": [
#     "https://api.envoy.com"
#   ],
#   "packages": [],
#   "uuid": "64bcc7c1-ce82-4fee-b676-7cbc1a0981d0",
#   "sub_type": "third_party"
# }

# i want to get these data and remove the version and uuid keys and put all of them in one json file

def get_all_jsons_files(jsons_files_path: str) -> list:
    return [os.path.join(jsons_files_path, file) for file in os.listdir(jsons_files_path) if file.endswith(".json")]

def store_all_data_in_one_file(jsons_files_path: str):
    all_jsons_files = get_all_jsons_files(jsons_files_path)
    all_data = []
    package_managers = set()
    deleted_components = []
    for file in all_jsons_files:
        data = read_json_file(file)
        data.pop("metadata")
        data.pop("uuid")
        data["id"] = str(uuid.uuid4())
        package_manager = None
        packages = []
        for package in data["packages"]:
            package_managers.add(package["package_manager"])
            package_manager = package["package_manager"]
            if package_manager and package_manager not in ["pypi", "go", "rubygems", "maven", "packagist", "nuget"]:
                packages.append(package)
        data["packages"] = packages
        if len(packages) == 0 and len(data["urls"]) == 0:
            deleted_components.append(data["name"])
            continue
        all_data.append(data)
    print(package_managers)
    print(deleted_components)
    print(len(all_data))
    with open(os.path.join(protego_workspace_dir, "src/core/detectors/classification/third_parties/cleaned.json"), "w") as file:
        json.dump(all_data, file, indent=4)

store_all_data_in_one_file(jsons_files_path)


def store_suitable_datastructures():
    uuid_to_service: dict[str, dict] = {}
    url_to_uuid: dict[str, str] = {}
    npm_package_to_uuid: dict[str, str] = {}
    nuget_package_to_uuid: dict[str, str] = {}
    all_data = read_json_file(os.path.join(protego_workspace_dir, "src/core/detectors/classification/third_parties/cleaned.json"))
    for data in all_data:
        uuid_to_service[data["id"]] = data
        for url in data["urls"]:
            url_to_uuid[url] = data["id"]
        for package in data["packages"]:
            if package["package_manager"] == "npm":
                npm_package_to_uuid[package["name"]] = data["id"]
    with open(os.path.join(protego_workspace_dir, "src/core/detectors/classification/third_parties/uuid_to_service.json"), "w") as file:
        json.dump(uuid_to_service, file, indent=4)
    with open(os.path.join(protego_workspace_dir, "src/core/detectors/classification/third_parties/url_to_uuid.json"), "w") as file:
        json.dump(url_to_uuid, file, indent=4)
    with open(os.path.join(protego_workspace_dir, "src/core/detectors/classification/third_parties/npm_package_to_uuid.json"), "w") as file:
        json.dump(npm_package_to_uuid, file, indent=4)


store_suitable_datastructures()

