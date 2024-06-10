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
from patterns_reader import known_persons_object_patterns,  \
                known_object_patterns, \
                unknown_object_patterns, \
                unknown_object_extended_patterns, \
                associated_object_patterns, \
                known_data_object_patterns, \
                user_identifier_patterns, \
                    get_category_group_name, \
                    add_category_group_name_to_classification, \
                    normalize_object




# Enhanced classify_object function
def classify_object(obj_name: str, attributes: dict[str, Any]):
    obj_name, attributes = normalize_object(obj_name, attributes)
    classification = {}

    object_type = "unknown"
    for known_person_obj in known_persons_object_patterns:
        if re.search(known_person_obj["include_regexp"], obj_name, re.IGNORECASE):
            object_type = "known"
            break


    if object_type == "known":
        # Apply known object patterns
        for attr_name, attr_type in attributes.items():
            for pattern, data_type in known_object_patterns.items():
                if re.search(pattern, attr_name, re.IGNORECASE):
                    classification[attr_name] = data_type
                    break
        return classification
    else:
        # Apply unknown object patterns
        positive_unknown_object_patterns = False
        for attr_name, attr_type in attributes.items():
            for pattern, data_type in unknown_object_patterns.items():
                if re.search(pattern, attr_name, re.IGNORECASE):
                    classification[attr_name] = data_type
                    positive_unknown_object_patterns = True
                    break
        
        if positive_unknown_object_patterns:
            # Apply unknown object extended patterns for the remaining unclassified attributes
            for attr_name, attr_type in attributes.items():
                if attr_name not in classification:
                    for pattern, data_type in unknown_object_extended_patterns.items():
                        if re.search(pattern, attr_name, re.IGNORECASE):
                            classification[attr_name] = data_type
                            break

            return classification

        else:
            # Apply user identifier patterns
            positive_user_identifier_patterns = False
            for attr_name in attributes:
                for pattern in user_identifier_patterns:
                    if re.search(pattern, attr_name, re.IGNORECASE):
                        classification[attr_name] = 'User Identifier'
                        positive_user_identifier_patterns = True
                        break
            
            if not positive_user_identifier_patterns:
                return classification
            
            else:
                # Apply associated object patterns
                positive_associated_object_patterns = False
                for attr in attributes:
                    for pattern, data_type in associated_object_patterns.items():
                        if re.search(pattern, attr, re.IGNORECASE):
                            classification[attr] = data_type
                            positive_associated_object_patterns = True
                            break
                
                if positive_associated_object_patterns:
                    return classification
                
                if not positive_associated_object_patterns:
                    # Apply known data object patterns as a last resort
                    for pattern, data_type in known_data_object_patterns.items():
                        if re.search(pattern, attr_name, re.IGNORECASE):
                            classification[attr_name] = data_type
                            break
                
                return classification

    return classification


attributes = {
    'zeby_manga': 'integer',
    'user_id': 'integer',
    'notification_enabled': 'boolean',
    'user_name': 'string'
}


if __name__ == "__main__":
    
    classification = classify_object('ads', attributes)
    print(classification)
    classification = add_category_group_name_to_classification(classification)
    
