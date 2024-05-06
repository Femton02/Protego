import os
import sys

protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

from typing import Any
from enum import Enum
from rule_parser import read_rules_from_yaml

class FilterType(Enum):
    HELPER_PATTERN = 'detection'
    REGEX = 'regex'
    VALUES = 'values'

class Filter:
    def __init__(self, variable: str, filter_type: FilterType, filter_method: Any) -> None:
        self.variable = variable
        self.type: FilterType = filter_type
        self.method: Any = filter_method

    def __str__(self) -> str:
        return f"Filter: {self.variable}, {self.type}, {self.method}"

class Pattern:
    def __init__(self, data, id):
        self.id = id
        self.pattern = data.get('pattern', '')
        self.filters = data.get('filters', [])
        self.process_filters()
        self.query = ''
        self.variables = {}
        self.content = {}
        self.types = {}

    def __str__(self):
        return f"Pattern: {self.id}, {self.pattern}"
    
    def process_filters(self):
        # convert list of filters to a dictionary with variable name as key and detection as value
        new_filters = {}
        for filter in self.filters:
            if filter['variable'] not in new_filters:
                new_filters[filter['variable']] = []
            
            found_filter = False
            for filter_type in FilterType:
                if filter_type.value in filter:
                    filter_obj = Filter(filter['variable'], filter_type, filter[filter_type.value])
                    new_filters[filter_obj.variable].append(filter_obj)
                    found_filter = True
                    break
            
            if not found_filter:
                raise Exception(f"Error in reading filter in yaml file: \nFor pattern {self.id}, filter {filter} is not in the correct format")
            


        self.filters = new_filters



    
class HelperPattern:
    def __init__(self, data):
        self.id = data.get('id', '')
        self.patterns = [Pattern(pattern, self.id + str(index)) for index, pattern in enumerate(data.get('patterns', []))]

    def __str__(self):
        return f"Helper Pattern: {self.id}"

class Rule:
    def __init__(self, data):
        self.metadata = data.get('metadata', {})
        self.id = self.metadata.get('id', '')
        self.languages = data.get('languages', [])

        self.patterns = [Pattern(pattern, self.id + str(index)) for index, pattern in enumerate(data.get('patterns', []))]
        
        self.helper_patterns = {}
        for helper_pattern in data.get('helper_patterns', []):
            helper_pattern_obj = HelperPattern(helper_pattern)
            self.helper_patterns[helper_pattern_obj.id] = helper_pattern_obj

        self.severity = self.metadata.get('severity', '')
        self.description = self.metadata.get('description', '')
        self.message = self.metadata.get('message', '')


    def __str__(self):
        return f"Rule: {self.metadata.get('id')}"

#____________________________________________________________________________________#
#                                   ENTRY POINT
#____________________________________________________________________________________#   


if __name__ == "__main__":
    #rule = Rule(read_rules_from_yaml(protego_workspace_dir + "/test/rules/rule.yaml"))
    rule = process_rule(protego_workspace_dir + "/test/rules/rule.yaml")

    # Accessing rule attributes

    print(rule)
