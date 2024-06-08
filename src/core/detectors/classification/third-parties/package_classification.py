import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#



npm_packages_to_uuid = read_json_file(os.path.join(protego_workspace_dir, "src/core/detectors/classification/third-parties/db/npm_packages_to_uuid.json"))
uuid_to_service = read_json_file(os.path.join(protego_workspace_dir, "src/core/detectors/classification/third-parties/db/uuid_to_service.json"))

def classify_package(package: str, package_manager: str) -> dict | None:

    if package_manager == "npm":
        packages_to_uuid = npm_packages_to_uuid
    else:
        return None

    service_uuid = packages_to_uuid.get(package)
    if not service_uuid:
        return None
    return uuid_to_service[service_uuid]

def test_classify_package():
    assert classify_package("stripe", "npm") == {
        "name": "Stripe",
        "type": "external_service",
        "urls": [
            "https://api.stripe.com",
            "https://js.stripe.com"
        ],
        "packages": [
            {
                "name": "stripe",
                "group": None,
                "package_manager": "npm"
            },
            {
                "name": "react-stripe-elements",
                "group": None,
                "package_manager": "npm"
            },
            {
                "name": "@stripe/stripe-js",
                "group": None,
                "package_manager": "npm"
            },
            {
                "name": "@stripe/react-stripe-js",
                "group": None,
                "package_manager": "npm"
            }
        ],
        "sub_type": "third_party",
        "id": "39c86933-162f-4ae2-8da7-759892460d45"
    }
    assert classify_package("stripe", "nuget") == None
    assert classify_package("stripe", "pip") == None
    assert classify_package("stripe", "yarn") == None
    



if __name__ == "__main__":
    print("Running tests...")
    test_classify_package()
    print("All tests passed.")