import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#


from core.detectors.components_detection import detect_components, classify_components
from core.detectors.datatypes_detection import detect_datatypes

def get_datatypes_in_project(root_dir_path: str):
    js_files = []
    for root, _, files in os.walk(os.path.dirname(root_dir_path)):
        for file in files:
            if file.endswith('.js'):
                js_files.append(os.path.join(root, file))
    datatypes = {}
    for js_file in js_files:
        with open(js_file, 'r') as f:
            content = f.read()
        tree = parse_js_code(content)
        res = detect_datatypes(tree)
        datatypes[js_file] = res
    return datatypes

def get_deps_in_project(root_dir_path: str):
    urls, npm_deps, yarn_deps = detect_components(root_dir_path)
    return npm_deps + yarn_deps

def get_all_in_project(root_dir_path: str):
    urls, npm_deps, yarn_deps = detect_components(root_dir_path)
    classified = classify_components(urls, npm_deps, yarn_deps)
    datatypes = get_datatypes_in_project(root_dir_path)
    return classified, datatypes, npm_deps + yarn_deps, urls

def generate_privacy_report(root_dir_path: str):
    classified, datatypes, deps, urls = get_all_in_project(root_dir_path)
    return {
        "datatypes": datatypes,
        "classified": classified,
        "deps": deps, 
        "unclassified_external_services": urls
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python privacy_scanner.py <path_to_project>")
        sys.exit(1)
    root_dir_path = sys.argv[1]
    report = generate_privacy_report(root_dir_path)
    print(json.dumps(report, indent=4))