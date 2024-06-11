import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#


from core.detectors.npm.npm_config import NpmConfig
from core.detectors.yarn.yarn_config import YarnConfig
from core.detectors.urls.urls_detector import URLDetector
from core.detectors.classification.third_parties.package_classification import classify_package
from core.detectors.classification.third_parties.url_classification import classify_url
import os


def detect_urls(root_dir_path: str):
    
    # walk all the js files and detect urls
    js_files = []
    for root, _, files in os.walk(os.path.dirname(root_dir_path)):
        for file in files:
            if file.endswith('.js'):
                js_files.append(os.path.join(root, file))
    urls = []
    
    for js_file in js_files:
        with open(js_file, 'r') as f:
            content = f.read()
        tree = parse_js_code(content)
        print(js_file)
        detector = URLDetector(tree, js_file)
        urls += detector.detect()

    return urls
    

def detect_deps(root_dir_path: str):
    npm_config = NpmConfig(root_dir_path)
    yarn_config = YarnConfig(root_dir_path)
    npm_deps = npm_config.detect() or []
    yarn_deps = yarn_config.detect() or []
    return npm_deps, yarn_deps

def detect_components(root_dir_path: str):
    urls = detect_urls(root_dir_path)
    npm_deps, yarn_deps = detect_deps(root_dir_path)
    return urls, npm_deps, yarn_deps

def classify_components(urls, npm_deps, yarn_deps):
    classified_urls = [classify_url(url) for url in urls]
    classified_deps = [classify_package(dep, 'npm') for dep in npm_deps] + [classify_package(dep, 'yarn') for dep in yarn_deps]
    return classified_urls + classified_deps
    

if __name__ == "__main__":
    urls, npm_deps, yarn_deps = detect_components(os.path.join(protego_workspace_dir, "testcode/"))
    components = classify_components(urls, npm_deps, yarn_deps)

    print(json.dumps(components, indent=4))
