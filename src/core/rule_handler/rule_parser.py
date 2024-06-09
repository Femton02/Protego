import os
import sys
import ruamel.yaml as yaml

protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

def read_rules_from_yaml(rule_file_path: str) -> dict:
    """
    Function to read rules from a YAML file.
    """
    try:
        with open(rule_file_path, "r", encoding="utf-8") as file:
            rules = yaml.safe_load(file)
            return rules
    except FileNotFoundError:
        print(f"Error: Rule file '{rule_file_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error: Error reading rule file '{rule_file_path}': {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

def process_rule(rulepath: str): 
    rule = Rule(read_rules_from_yaml(rulepath))
    for pattern_obj in rule.patterns:
        query, var, content, types = parse_pattern(pattern_obj.pattern)
        pattern_obj.query = query
        pattern_obj.variables = var
        pattern_obj.content = content
        pattern_obj.types = types
    for helper_pattern_obj in rule.helper_patterns.values():
        for pattern_obj in helper_pattern_obj.patterns:
            query, var, content, types = parse_pattern(pattern_obj.pattern)
            pattern_obj.query = query
            pattern_obj.variables = var
            pattern_obj.content = content
            pattern_obj.types = types

    return rule    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rule_parser.py <rule_file>")
        sys.exit(1)

    rulepath = sys.argv[1]
    process_rule(rulepath)
    print("Rule processed successfully.")
