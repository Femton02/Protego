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
from typing import Any

# Sample data classification patterns
data_classification_patterns = [
    {
        "metadata": {"version": "1.0"},
        "id": 1,
        "data_type_uuid": "22e24c62-82d3-4b72-827c-e261533331bd",
        "exclude_regexp": r"\b(.*(notification|config(uration)?|template|enabled|token|reminder|subject|body|handover|sent.by|settings?|accept|label|id|voice|type).*|required)\b",
        "exclude_types": ["boolean", "date", "number"],
        "friendly_name": "Email Address",
        "health_context_data_type_uuid": None,
        "include_regexp": "\\b.*email.*\\b",
        "match_column": True,
        "match_object": False,
        "object_type": ["known", "unknown_extended"]
    },
    # Add more patterns here...
]

# Sample data categories
data_categories = [
    {
        "metadata": {"version": "1.0"},
        "name": "Authenticating",
        "uuid": "dd88aee5-9d40-4ad2-8983-0c791ddec47c"
    },
    # Add more data categories here...
]

# Sample category groupings
category_groupings = {
    "groups": {
        "e1d3135b-3c0f-4b55-abce-19f27a26cbb3": {
            "name": "Personal Data",
            "parent_uuids": []
        },
        "f6a0c071-5908-4420-bac2-bba28d41223e": {
            "name": "Personal Data (Sensitive)",
            "parent_uuids": []
        },
        "247fa503-115b-490a-96e5-bcd357bd5686": {
            "name": "PHI",
            "parent_uuids": [
                "e1d3135b-3c0f-4b55-abce-19f27a26cbb3"
            ]
        },
        "172d90e3-cb9a-46b6-90e5-dd7169c3af54": {
            "name": "PII",
            "parent_uuids": [
                "e1d3135b-3c0f-4b55-abce-19f27a26cbb3"
            ]
        }
    },
    "category_mapping": {
        "dd88aee5-9d40-4ad2-8983-0c791ddec47c": {
            "name": "Authenticating",
            "group_uuids": [
                "172d90e3-cb9a-46b6-90e5-dd7169c3af54"
            ]
        },
        "8099225c-7e49-414f-aac2-e7045379bb40": {
            "name": "Behavioral Information",
            "group_uuids": [
                "e1d3135b-3c0f-4b55-abce-19f27a26cbb3"
            ]
        },
        "79a36d6e-c5ca-4f61-ba53-0d7ad42cbe5a": {
            "name": "Communication",
            "group_uuids": [
                "172d90e3-cb9a-46b6-90e5-dd7169c3af54",
                "247fa503-115b-490a-96e5-bcd357bd5686"
            ]
        }
    }
}



def read_data_classification_patterns():
    # read data classification patterns from a folder called db/data_type_classification_patterns/*.json
    data_classification_patterns = []
    patterns_dir = os.path.join(protego_workspace_dir, "src/core/detectors/classification/datatypes/db/data_type_classification_patterns")
    for file in os.listdir(patterns_dir):
        if file.endswith(".json"):
            with open(os.path.join(patterns_dir, file), 'r') as f:
                data = json.load(f)
                data_classification_patterns.append(data)
    
    # Check patterns compilation for errors
    for pattern in data_classification_patterns:
        try:
            re.compile(pattern["include_regexp"])
        except re.error as e:
            print(f"Error compiling pattern {pattern['include_regexp']}: {e}")
            sys.exit(1)
        except e:
            pass
        try:
            re.compile(pattern["exclude_regexp"])
        except re.error as e:
            print(f"Error compiling pattern {pattern['exclude_regexp']}: {e}")
            sys.exit(1)
        except:
            pass

    return data_classification_patterns



def read_data_types():
    data_types = {}
    types_dir = os.path.join(protego_workspace_dir, "src/core/detectors/classification/datatypes/db/data_types")
    for file in os.listdir(types_dir):
        if file.endswith(".json"):
            with open(os.path.join(types_dir, file), 'r') as f:
                data = json.load(f)
                data_types[data["uuid"]] = data
    return data_types



def read_data_categories():
    data_categories = {}
    categories_dir = os.path.join(protego_workspace_dir, "src/core/detectors/classification/datatypes/db/data_categories")
    for file in os.listdir(categories_dir):
        if file.endswith(".json"):
            with open(os.path.join(categories_dir, file), 'r') as f:
                data = json.load(f)
                data_categories[data["uuid"]] = data
    return data_categories


def read_category_groupings():
    category_groupings = {}
    groupings_dir = os.path.join(protego_workspace_dir, "src/core/detectors/classification/datatypes/db/")
    for file in os.listdir(groupings_dir):
        if file.endswith(".json"):
            with open(os.path.join(groupings_dir, file), 'r') as f:
                data = json.load(f)
                category_groupings.update(data)
    return category_groupings

def read_known_persons_object_patterns():
    known_persons_object_patterns = []
    patterns_dir = os.path.join(protego_workspace_dir, "src/core/detectors/classification/datatypes/db/known_person_object_patterns")
    for file in os.listdir(patterns_dir):
        if file.endswith(".json"):
            with open(os.path.join(patterns_dir, file), 'r') as f:
                data = json.load(f)
                known_persons_object_patterns.append(data)

    for pattern in known_persons_object_patterns:
        try:
            re.compile(pattern["include_regexp"])
        except re.error as e:
            print(f"Error compiling pattern {pattern['include_regexp']}: {e}")
            sys.exit(1)
    return known_persons_object_patterns

def read_other_patterns(data_type_classification_patterns):
    known_object_patterns = {}
    unknown_object_patterns = {}
    unknown_object_extended_patterns = {}
    associated_object_patterns = {}
    known_data_object_patterns = {}

    for pattern in data_type_classification_patterns:
        if "known" in pattern["object_type"]:
            known_object_patterns[pattern["include_regexp"]] = pattern
        if "unknown" in pattern["object_type"]:
            unknown_object_patterns[pattern["include_regexp"]] = pattern
        if "unknown_extended" in pattern["object_type"]:
            unknown_object_extended_patterns[pattern["include_regexp"]] = pattern
        if "associated" in pattern["object_type"]:
            associated_object_patterns[pattern["include_regexp"]] = pattern
        if "known_data_object" in pattern["object_type"]:
            known_data_object_patterns[pattern["include_regexp"]] = pattern

        try:
            re.compile(pattern["include_regexp"])
        except re.error as e:
            print(f"Error compiling pattern {pattern['include_regexp']}: {e}")
            sys.exit(1)
    
    patterns = {
        "known_object_patterns": known_object_patterns,
        "unknown_object_patterns": unknown_object_patterns,
        "unknown_object_extended_patterns": unknown_object_extended_patterns,
        "associated_object_patterns": associated_object_patterns,
        "known_data_object_patterns": known_data_object_patterns
    }
    return patterns


category_groupings = read_category_groupings()
data_categories = read_data_categories()
data_types = read_data_types()

known_persons_object_patterns = read_known_persons_object_patterns()
data_classification_patterns = read_data_classification_patterns()
other_patterns = read_other_patterns(data_classification_patterns)
known_object_patterns = other_patterns["known_object_patterns"]
unknown_object_patterns = other_patterns["unknown_object_patterns"]
unknown_object_extended_patterns = other_patterns["unknown_object_extended_patterns"]
associated_object_patterns = other_patterns["associated_object_patterns"]
known_data_object_patterns = other_patterns["known_data_object_patterns"]


# TODO: where to get these patterns from?    
user_identifier_patterns = [r'\buser(id)?\b', r'\bemail\b']


def get_category_group_name(category_uuid):
    # Function to get category group name by UUID
    if category_uuid in category_groupings["category_mapping"]:
        group_uuids = category_groupings["category_mapping"][category_uuid]["group_uuids"]
        group_names = [category_groupings["groups"][uuid]["name"] for uuid in group_uuids]
        return group_names
    return []

def add_category_group_name_to_classification(classification: dict[str, Any]):
    new_classification = {}
    for attr_name in classification.keys():
        attr_type = classification[attr_name]
        data_type_uuid = attr_type["data_type_uuid"]
        data_type = data_types[data_type_uuid]
        category_uuid = data_type["category_uuid"]
        group_names = get_category_group_name(category_uuid)
        classification[attr_name]["group_names"] = group_names
        classification[attr_name]["category"] = data_categories[category_uuid]["name"]
        classification[attr_name]["data_type"] = data_type["name"]

        # remove unnecessary keys
        classification[attr_name].pop("metadata", None)
        classification[attr_name].pop("exclude_regexp", None)
        classification[attr_name].pop("exclude_types", None)
        classification[attr_name].pop("id", None)
        classification[attr_name].pop("object_type", None)
        classification[attr_name].pop("match_column", None)
        classification[attr_name].pop("match_object", None)
        classification[attr_name].pop("include_regexp", None)
        classification[attr_name].pop("health_context_data_type_uuid", None)

        for group_name in group_names:
            if group_name not in new_classification:
                new_classification[group_name] = []
            new_classification[group_name].append(classification[attr_name])
    return new_classification


def normalize_object(obj_name: str, attributes: dict[str, str]):
    obj_name = obj_name.lower().replace("_", " ").replace("-", " ")
    normalized_attributes = {}
    for attr_name, attr_value in attributes.items():
        attr_name = attr_name.lower().replace("_", " ").replace("-", " ")
        normalized_attributes[attr_name] = attr_value
    return obj_name, normalized_attributes


if __name__ == "__main__":
    pass