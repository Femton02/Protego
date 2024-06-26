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

def compare_variables(match: dict[str, Node], pattern: Pattern, helper_patterns: list[HelperPattern]):
    variables = pattern.variables
    types = pattern.types
    for key, value in variables.items():
        comparestr = "param" + str(key)
        if comparestr not in match:
            return False
        node = match[comparestr]
        if not check_type(types, value, node):
            return False

        variable_name = value
        filters = pattern.filters[variable_name]
        for filter in filters:
            if filter.type == FilterType.HELPER_PATTERN:
                helper_pattern_id = filter.method
                helper_pattern = helper_patterns[helper_pattern_id]
                helper_pattern_results = get_matches(node.text.decode(), helper_pattern.patterns, helper_patterns)
                if not helper_pattern_results:
                    return False
            # TODO: Handle other filter types
        


    return True

def trace_focus(focus: dict, match: dict[str, Node], parsed_src_code_tree: Tree):
    comparestr = ""
    for key, value in focus.items():
        comparestr = "focus" + str(key)
    if comparestr not in match:
        return False
    node = match[comparestr]
    if value[1] == "LITERAL":
        if node.text.decode() != value[1]:
            return False
        #look for the variable in the whole src code, then look for another operands in the same line and focus on them
        varquery = "((identifier) @focus (#eq? @focus \""+value[0]+"\"))"
        return True
    else:
        #look for the variable in the whole src code, then look for another operands in the same line and focus on them
        varquery = "((identifier) @focus (#eq? @focus \""+node.text.decode()+"\"))"
        return True
    return True

def get_matches(src_code: str, patterns: list[Pattern], helper_patterns: list[HelperPattern]):
    parsed_src_code_tree = parse_js_code(src_code)
    result = []
    for pattern in patterns:
        print(f"Querying pattern: {pattern.id}")
        _, matches = query_tree(parsed_src_code_tree, pattern.query)

        for x in matches:
            match = x[1]
            if not compare_content(pattern.content, match):
                # print(f"Content Mismatch for match \n{match}\nand pattern \n{pattern}\n")
                continue
            if not compare_variables(match, pattern, helper_patterns):
                # print(f"Type or variable Mismatch for match \n{match}\nand pattern \n{pattern}\n")
                continue
            if not trace_focus(pattern.focus, match, parsed_src_code_tree):
                # print(f"Focus Mismatch for match \n{match}\nand pattern \n{pattern}\n")
                continue

            # print(f"Found match: {match} for pattern {pattern}")
            result.append(match)
    
    return result



if __name__ == "__main__":
    rule = process_rule(protego_workspace_dir + "/rules/rule.yaml")
    src_code = "const html = `<div>${event.name}</div>`;\nconst someRandomStuff = {\n  // ok: tainted-html-response\n  data: event.foo\n}\nbar(someRandomStuff)\nvar zzz = html;\nconst response = {\n  statusCode: 200,\n  // ruleid: tainted-html-response\n  body: zzz,\n  headers: {\n    'Content-Type': 'text/html',\n  }\n};"
    matches = get_matches(src_code, rule.patterns, rule.helper_patterns)
    print(f"Matches: {matches}")