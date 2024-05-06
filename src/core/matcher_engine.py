import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#


def compare_content(content: dict, match: dict[str, Node]):
    for key, value in content.items():
        comparestr = "param" + str(key)
        if comparestr not in match:
            return False
        node = match[comparestr]
        if node.text.decode() != value:
            return False
    return True

def check_type(types: dict, variable_name: str, node: Node):
    if variable_name in types:
        if types[variable_name] != node.type:
            return False
    return True

def compare_variables(variables: dict, types: dict, match: dict[str, Node]):
    for key, value in variables.items():
        comparestr = "param" + str(key)
        if comparestr not in match:
            return False
        node = match[comparestr]
        if not check_type(types, value, node):
            return False
        # TODO: get the filters for this variable and process it
    return True

def get_matches(parsed_src_code_tree: Tree, rule: Rule):
    result = []
    for pattern in rule.patterns:
        _, matches = query_tree(parsed_src_code_tree, pattern.query)

        for x in matches:
            match = x[1]
            if not compare_content(pattern.content, match):
                print(f"Content Mismatch for match \n{match}\n and pattern \n{pattern}\n")
                continue
            if not compare_variables(pattern.variables, pattern.types, match):
                print(f"Type or variable Mismatch for match \n{match}\n and pattern \n{pattern}\n")
                continue

            print(f"Found match: {match} for pattern {pattern}")
            result.append(match)
    
    return result



if __name__ == "__main__":
    rule = process_rule(protego_workspace_dir + "/test/rules/rule.yaml")
    src_code = "{\ncookie: { httpOnly: false }\n}"
    parsed_src_code_tree = parse_js_code(src_code)
    matches = get_matches(parsed_src_code_tree, rule)

