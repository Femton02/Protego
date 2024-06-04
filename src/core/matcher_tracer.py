import os
import sys

protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#
from core.report_engine import read_file
from core.protego_node import ProtegoTree
from core.symbol_table import SymbolTableBuilder

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
                helper_pattern_results = get_pre_run_matches(node, helper_pattern.patterns, helper_patterns)
                if not helper_pattern_results:
                    return False
            # TODO: Handle other filter types
    return True

def get_pre_run_matches(parsed_src_code, patterns: list[Pattern], helper_patterns: list[HelperPattern]):
    result = []
    for pattern in patterns:
        print(f"Querying pattern: {pattern.id}")
        _, matches = query_tree(parsed_src_code, pattern.query)
        for x in matches:
            match = x[1]
            if not compare_content(pattern.content, match):
                # print(f"Content Mismatch for match \n{match}\nand pattern \n{pattern}\n")
                continue
            if not compare_variables(match, pattern, helper_patterns):
                # print(f"Type or variable Mismatch for match \n{match}\nand pattern \n{pattern}\n")
                continue
            # print(f"Found match: {match} for pattern {pattern}")
            result.append(match)
    return result


if __name__ == "__main__":
    rule = process_rule("test/express/insecure-cookie/testdata/focus_test.yaml")
    src_code = read_file("test/express/insecure-cookie/testdata/focus_test.js")
    # pre run all the helper patterns
    parsed_src_code = parse_js_code(src_code)
    # create our own tree to be able to make the symbol table and trace the variables
    proTree = ProtegoTree(parsed_src_code)

    node_map = proTree.node_mapping
    # create the symbol table
    symbol_table = SymbolTableBuilder()
    aliases = symbol_table.root_symbol_table.aliases
    symbol_table.build(proTree)
    pre_caught_nodes = get_pre_run_matches(parsed_src_code.root_node, rule.patterns, rule.helper_patterns)
    print("done")
    # print("__________________________")
    # for node_id in pre_caught_nodes:
    #     print(node_map[node_id])
    #     print(pre_caught_nodes[node_id])
    #     print("__________________________")
    # print("done")
    