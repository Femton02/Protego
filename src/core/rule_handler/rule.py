import os
import sys

protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

from rule_parser import read_rules_from_yaml
class Pattern:
    def __init__(self, data, id):
        self.id = id
        self.pattern = data.get('pattern', '')
        self.filters = data.get('filters', [])
        self.query = ''
        self.variables = {}
        self.content = {}
        self.types = {}

    def __str__(self):
        return f"Pattern: {self.id}, {self.pattern}"

# TODO: Create a class for filters
    
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
        self.helper_patterns = [HelperPattern(helper_pattern) for helper_pattern in data.get('helper_patterns', [])]

        self.severity = self.metadata.get('severity', '')
        self.description = self.metadata.get('description', '')
        self.message = self.metadata.get('message', '')


    def __str__(self):
        return f"Rule: {self.metadata.get('name')}"


if __name__ == "__main__":
    rule = Rule(read_rules_from_yaml(protego_workspace_dir + "/test/rules/rule.yaml"))
    # Accessing rule attributes
    print(rule)
    print("Patterns:", rule.patterns)
    print("Languages:", rule.languages)
    print("Helper Patterns:", rule.helper_patterns)
    print("Metadata:", rule.metadata)
