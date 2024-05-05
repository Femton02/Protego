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

rules = read_rules_from_yaml("../../test/rules/rule.yaml")
print(rules)