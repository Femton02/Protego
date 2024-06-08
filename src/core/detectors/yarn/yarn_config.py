import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#

from detectors.detector_interface import DetectorInterface, DependencyDetectionResult
import json
import re


yarn_config_files = ["yarn.lock"]


class YarnConfigResult(DependencyDetectionResult):
    """Result of the detection."""

    detector_name: str = "YarnConfig"

    

class YarnConfig(DetectorInterface):
    """Detector for yarn configuration files like yarn.lock."""


    def __init__(self, root_dir_path: str):

        if not os.path.exists(root_dir_path):
            raise FileNotFoundError(f"The root directory path '{root_dir_path}' does not exist.")
        self.root_dir_path = root_dir_path

        self.results: list[YarnConfigResult] = []
        self.files_to_search = []

    def detect(self):
        """Detects dependencies in projects that use yarn from the yarn configuration files like yarn.lock."""
        self._discover_yarn_config_files()
        self._read_yarn_config_files()
    
    def get_results(self):
        """Gets the results of the detection."""
        return self.results
    
    def _discover_yarn_config_files(self) -> None:
        """Searches for yarn configuration files in the root directory."""
        
        for dirpath, _, filenames in os.walk(self.root_dir_path):
            for filename in filenames:
                if filename in yarn_config_files:
                    self.files_to_search.append(os.path.join(dirpath, filename))
        
        if not self.files_to_search:
            print("No yarn configuration files found.")
        else:
            print(f"Found {len(self.files_to_search)} yarn configuration files.")

    def _read_yarn_config_files(self) -> None:
        """Reads the yarn configuration files to extract dependencies."""
        
        for file_path in self.files_to_search:
            file_name = os.path.basename(file_path)
            match file_name:
                case "yarn.lock":
                    self._extract_deps_from_yarn_lock(file_path)
                case _:
                    raise ValueError(f"Expected a yarn configuration file, but got '{file_name}'.")
    
    def _extract_deps_from_yarn_lock(self, file_path: str) -> None:
        """Extracts dependencies from yarn.lock"""
        
        with open(file_path, "r") as file:
            dependencies = {}
            content = file.read()
            
            # Regular expression to find package entries
            pattern = re.compile(r'([^\s]+)@\^?[^\s]+:\n\s+version "([^"]+)"')
            matches = pattern.findall(content)
            
            for match in matches:
                package_name, version = match
                dependencies[package_name] = version

            print(f"Found {len(dependencies)} dependencies in {file_path}")
            for name, version in dependencies.items():
                result = YarnConfigResult(file_path=file_path, name=name, version=version)
                self.results.append(result)

    


    def _extract_deps_from_package_lock_json(self, file_path: str) -> None:
        """Extracts dependencies from package-lock.json."""
        
        
        with open(file_path, "r") as file:
            package_lock_json = json.load(file)
            dependencies = package_lock_json.get("dependencies", {})
            print(f"Found {len(dependencies)} dependencies in {file_path}")
            for name, details in dependencies.items():
                version = details.get("version")
                result = YarnConfigResult(file_path=file_path, name=name, version=version)
                self.results.append(result)
    
    def _extract_deps_from_yarn_shrinkwrap_json(self, file_path: str) -> None:
        """Extracts dependencies from yarn-shrinkwrap.json."""
        

        with open(file_path, "r") as file:
            yarn_shrinkwrap_json = json.load(file)
            dependencies = yarn_shrinkwrap_json.get("dependencies", {})
            print(f"Found {len(dependencies)} dependencies in {file_path}")
            for name, details in dependencies.items():
                version = details.get("version")
                result = YarnConfigResult(file_path=file_path, name=name, version=version)
                self.results.append(result)
    




if __name__ == "__main__":
    if len(sys.argv) == 2:
        yarn_config = YarnConfig(sys.argv[1])
    else:
        yarn_config = YarnConfig("src/core/detectors/yarn/test_data/")
    yarn_config.detect()
    results = yarn_config.get_results()
    # print(json.dumps(results, indent=4, default=lambda o: o.__dict__))
    print(f"Found {len(results)} dependencies.")