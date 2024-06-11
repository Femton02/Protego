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


urls_to_uuid = read_json_file(os.path.join(protego_workspace_dir, "src/core/detectors/classification/third_parties/db/url_to_uuid.json"))
uuid_to_service = read_json_file(os.path.join(protego_workspace_dir, "src/core/detectors/classification/third_parties/db/uuid_to_service.json"))
def classify_url(url: str) -> dict | None:
    service_uuid = None
    # the urls are regex patterns
    for pattern, uuid in urls_to_uuid.items():
        pattern = pattern.replace("*", r".*")
        pattern = pattern + r".*"
        if re.match(pattern, url):
            service_uuid = uuid
            break
    if not service_uuid:
        return None
    return uuid_to_service[service_uuid]

def test_classify_url():
    assert classify_url("https://live.adyen.com/afsdaas/asd") == {
        "name": "Adyen",
        "type": "external_service",
        "urls": [
            "https://live-us.adyen.com",
            "https://live-au.adyen.com",
            "https://live.adyen.com",
            "https://test.adyen.com",
            "https://live.adyenpayments.com",
            "https://pal-test.adyen.com",
            "https://checkout-test.adyen.com"
        ],
        "packages": [],
        "sub_type": "third_party",
        "id": "1f10bf7f-c141-431d-a81f-06a81833b649"
    }
    assert classify_url("https://api.stripe.com/v1/charges") == {
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
    assert classify_url("https://fsadasd.tencentcloudapi.com/safd") == {
        "name": "Tencent Cloud APIs",
        "type": "external_service",
        "urls": [
            "https://tencentcloudapi.com",
            "https://*.tencentcloudapi.com"
        ],
        "packages": [],
        "sub_type": "third_party",
        "id": "1c4d02a4-0ee6-43ee-8966-27cd96bbf9d3"
    }

print ("Running tests...")


test_classify_url()