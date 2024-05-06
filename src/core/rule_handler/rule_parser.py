from core.rule_handler.pattern_parser import parse_pattern
from .rule import Rule, Pattern, HelperPattern
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