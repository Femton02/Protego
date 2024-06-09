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
import re

class FilterType(Enum):
    HELPER_PATTERN = 'detection'
    REGEX = 'regex'
    VALUES = 'values'

class Filter:
    def __init__(self, variable: str, filter_type: FilterType, filter_method: Any, negation: bool = False) -> None:
        self.variable = variable
        self.type: FilterType = filter_type
        self.method: Any = filter_method
        self.negation = negation

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
        self.focus = {}

    def __str__(self):
        return f"Pattern: {self.id}, {self.pattern}"
    
    def process_filters(self):
        new_filters = {}
        for filter in self.filters:
            if 'either' in filter:
                for either_filter in filter['either']:
                    self._process_single_filter(either_filter, new_filters)
            else:
                self._process_single_filter(filter, new_filters)
        self.filters = new_filters

    def _process_single_filter(self, filter, new_filters):
        if isinstance(filter, list):
            for sub_filter in filter:
                self._process_single_filter(sub_filter, new_filters)
            return
        
        if 'not' in filter:
            negation = True
            filter = filter['not'][0]
        else:
            negation = False

        if filter['variable'] not in new_filters:
            new_filters[filter['variable']] = []
        
        found_filter = False
        for filter_type in FilterType:
            if filter_type.value in filter:
                filter_method = filter[filter_type.value]
                filter_obj = Filter(filter['variable'], filter_type, filter_method, negation)
                new_filters[filter_obj.variable].append(filter_obj)
                found_filter = True
                break
        
        if not found_filter:
            raise Exception(f"Error in reading filter in yaml file: \nFor pattern {self.id}, filter {filter} is not in the correct format")


def fix_regex(regex) -> str:
    # Look for any double backslashes and replace them with single backslashes
    fixed_regex = ""
    i = 0
    print(regex[0])
    while i < len(regex):
        if regex[i] == "\\" and i + 1 < len(regex) and regex[i + 1] == "\\":
            fixed_regex += regex[i]
            i += 2
        else:
            fixed_regex += regex[i]
            i += 1
    return fixed_regex

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
    rule = process_rule("test/express/insecure-cookie/testdata/filter_test.yaml")

    # Accessing rule attributes
    print(rule)