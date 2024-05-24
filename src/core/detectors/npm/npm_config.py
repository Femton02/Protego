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


npm_config_files = ["package.json", "package-lock.json", "npm-shrinkwrap.json"]


class NpmConfigResult(DependencyDetectionResult):
    """Result of the detection."""

    detector_name: str = "NpmConfig"

    

class NpmConfig(DetectorInterface):
    """Detector for npm configuration files like package.json."""


    def __init__(self, root_dir_path: str):

        if not os.path.exists(root_dir_path):
            raise FileNotFoundError(f"The root directory path '{root_dir_path}' does not exist.")
        self.root_dir_path = root_dir_path

        self.results: list[NpmConfigResult] = []
        self.files_to_search = []

    def detect(self):
        """Detects dependencies in projects that use npm from the npm configuration files like package.json."""
        self._discover_npm_config_files()
        self._read_npm_config_files()
    
    def get_results(self):
        """Gets the results of the detection."""
        return self.results
    
    def _discover_npm_config_files(self) -> None:
        """Searches for npm configuration files in the root directory."""
        
        for dirpath, _, filenames in os.walk(self.root_dir_path):
            for filename in filenames:
                if filename in npm_config_files:
                    self.files_to_search.append(os.path.join(dirpath, filename))
        
        if not self.files_to_search:
            print("No npm configuration files found.")
        else:
            print(f"Found {len(self.files_to_search)} npm configuration files.")

    def _read_npm_config_files(self) -> None:
        """Reads the npm configuration files to extract dependencies."""
        
        for file_path in self.files_to_search:
            file_name = os.path.basename(file_path)
            match file_name:
                case "package.json":
                    self._extract_deps_from_package_json(file_path)
                case "package-lock.json":
                    self._extract_deps_from_package_lock_json(file_path)
                case "npm-shrinkwrap.json":
                    self._extract_deps_from_npm_shrinkwrap_json(file_path)
                case _:
                    raise ValueError(f"Expected a npm configuration file, but got '{file_name}'.")
    
    def _extract_deps_from_package_json(self, file_path: str) -> None:
        """Extracts dependencies from package.json."""
        
        with open(file_path, "r") as file:
            package_json = json.load(file)
            dependencies = package_json.get("dependencies", {})
            dev_dependencies = package_json.get("devDependencies", {})
            peer_dependencies = package_json.get("peerDependencies", {})
            optional_dependencies = package_json.get("optionalDependencies", {})
            all_dependencies = {**dependencies, **dev_dependencies, **peer_dependencies, **optional_dependencies}
            print(f"Found {len(all_dependencies)} dependencies in {file_path}")
            for name, version in all_dependencies.items():
                version = re.sub(r"[\^~*]", "", version)
                result = NpmConfigResult(file_path=file_path, name=name, version=version)
                self.results.append(result)


    def _extract_deps_from_package_lock_json(self, file_path: str) -> None:
        """Extracts dependencies from package-lock.json."""
        
        
        with open(file_path, "r") as file:
            package_lock_json = json.load(file)
            dependencies = package_lock_json.get("dependencies", {})
            print(f"Found {len(dependencies)} dependencies in {file_path}")
            for name, details in dependencies.items():
                version = details.get("version")
                result = NpmConfigResult(file_path=file_path, name=name, version=version)
                self.results.append(result)
    
    def _extract_deps_from_npm_shrinkwrap_json(self, file_path: str) -> None:
        """Extracts dependencies from npm-shrinkwrap.json."""
        

        with open(file_path, "r") as file:
            npm_shrinkwrap_json = json.load(file)
            dependencies = npm_shrinkwrap_json.get("dependencies", {})
            print(f"Found {len(dependencies)} dependencies in {file_path}")
            for name, details in dependencies.items():
                version = details.get("version")
                result = NpmConfigResult(file_path=file_path, name=name, version=version)
                self.results.append(result)
    




if __name__ == "__main__":
    if len(sys.argv) == 2:
        npm_config = NpmConfig(sys.argv[1])
    else:
        npm_config = NpmConfig("src/core/detectors/npm/test_data/")
    npm_config.detect()
    results = npm_config.get_results()
    # print(json.dumps(results, indent=4, default=lambda o: o.__dict__))
    print(f"Found {len(results)} dependencies.")