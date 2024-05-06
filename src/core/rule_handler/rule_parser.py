import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *


import yaml

def read_rules_from_yaml(rule_file_path: str) -> dict:
    """
    Function to read rules from a YAML file.
    """
    try:
        with open(rule_file_path, "r") as file:
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
    for pattern in rule.patterns:
        query, var, content, types = parse_pattern(pattern.pattern)
        pattern.query = query
        pattern.variables = var
        pattern.content = content
        pattern.types = types


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rule_parser.py <rule_file>")
        sys.exit(1)

    rulepath = sys.argv[1]
    process_rule(rulepath)
    print("Rule processed successfully.")