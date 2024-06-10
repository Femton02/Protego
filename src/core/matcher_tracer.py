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
from core.protego_node import ProtegoTree, ProtegoNode
from core.symbol_table import SymbolTableBuilder, SymbolTable

parsed_src_code = None
node_map = None
symbol_table = None
proTree = None

def compare_content(content: dict, match: dict[str, Node]):
    for key, value in content.items():
        if key == -1:
            comparestr = "focus"
            if comparestr not in match:
                return False
            node = match[comparestr]
            if node.text.decode() != value:
                return False
        else:
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

def compare_variables(match: dict[str, Any], pattern: Pattern, helper_patterns: list[Any]) -> bool:
    if not pattern.variables:
        return True

    for variable_name, variable in pattern.variables.items():
        comparestr = "param" + str(variable_name)
        if comparestr not in match:
            return False
        node = match[comparestr]
        if not check_type(pattern.types, variable, node):
            return False
        if not handle_single_variable(variable, node, pattern.filters[variable], helper_patterns):
            return False
    return True

def handle_single_variable(variable: str, node: Any, filters: list[Filter], helper_patterns: list[Any]) -> bool:
    for filter in filters:
        if handle_single_filter(filter, node, helper_patterns):
            return True
    return False

def handle_single_filter(filter: Filter, node: Any, helper_patterns: list[Any]) -> bool:
    if filter.type == FilterType.HELPER_PATTERN:
        helper_pattern_id = filter.method
        helper_pattern = helper_patterns[helper_pattern_id]
        helper_pattern_results = run_matches(node, helper_pattern.patterns, helper_patterns)
        if filter.negation:
            return not helper_pattern_results
        else:
            return bool(helper_pattern_results)
    elif filter.type == FilterType.REGEX:
        re_pattern = filter.method
        match_result = re.match(re_pattern, node.text.decode())
        if filter.negation:
            return not match_result
        else:
            return bool(match_result)
    elif filter.type == FilterType.VALUES:
        for value in filter.method:
            if filter.negation:
                if node.text.decode() == value:
                    return False
            else:
                if node.text.decode() == value:
                    return True
        return filter.negation  # Return False if negation is False, True if negation is True
    return False

def check_trace(variable: Node, pattern: Pattern, helper_patterns: list[HelperPattern]):
    protego_var = node_map[variable.id]
    # Check if the variable source matches the pattern
    current_scope = protego_var.symbol_table
    while current_scope:
        if protego_var.text.decode() in current_scope.table:
            break
        current_scope = current_scope.parent
    if not current_scope:
        return None

    check_node = current_scope.table[protego_var.text.decode()]
    result = match_single_node(check_node.original_node, pattern, helper_patterns)
    if result:
        return result

    while check_node.points_to:
        check_node = check_node.points_to
        result = match_single_node(check_node.original_node, pattern, helper_patterns)
        if result:
            return result

    # Check aliases recursively
    return check_aliases_recursively(current_scope, variable.text.decode(), pattern, helper_patterns)

def check_aliases_recursively(symbol_table: SymbolTable, var_name: str, pattern: Pattern, helper_patterns: list[HelperPattern]):
    if var_name not in symbol_table.aliases:
        return None

    for alias in symbol_table.aliases[var_name]:
        if alias in symbol_table.table:
            check_node = symbol_table.table[alias]
            result = match_single_node(check_node.original_node, pattern, helper_patterns)
            if result:
                return result

            while check_node.points_to:
                check_node = check_node.points_to
                result = match_single_node(check_node.original_node, pattern, helper_patterns)
                if result:
                    return result

            # Recursively check aliases of the current alias
            result = check_aliases_recursively(symbol_table, alias, pattern, helper_patterns)
            if result:
                return result
    return None


def match_single_node(node: Node, pattern: Pattern, helper_patterns: list[HelperPattern]):
    captures, matches = query_tree(node, pattern.query)
    for x in matches:
        match = x[1]
        if not compare_content(pattern.content, match):
            continue
        if not compare_variables(match, pattern, helper_patterns):
            continue
        return match
    return None

def run_matches(parsed_src_code, patterns: list[Pattern], helper_patterns: list[HelperPattern]) -> list[Node]:
    result = []
    for pattern in patterns:
        #print(f"Querying pattern: {pattern.id}")
        if 'focus' in pattern.query:
            output = check_trace(parsed_src_code, pattern, helper_patterns)
            if output:
                result.append(output)
        _, matches = query_tree(parsed_src_code, pattern.query)
        for x in matches:
            match = x[1]
            if not compare_content(pattern.content, match):
                # print(f"Content Mismatch for match \n{match}\nand pattern \n{pattern}\n")
                continue
            # if 'focus' in match then we need to trace the focus, lookup that variable in the symbol table and check if its source matches the pattern.
            if not compare_variables(match, pattern, helper_patterns):
            # print(f"Type or variable Mismatch for match \n{match}\nand pattern \n{pattern}\n")
                continue
            # print(f"Found match: {match} for pattern {pattern}")
            result.append(match)
    return result

def get_matches(protego_tree: ProtegoTree, rule: Rule) -> list[ProtegoNode]:

    # create the symbol table
    symbol_table = SymbolTableBuilder()
    symbol_table.build(protego_tree.root)
    caught_nodes = run_matches(protego_tree.root.tree_sitter_node, rule.patterns, rule.helper_patterns)
    print("__________________________")
    print("Number of caught nodes: ", len(caught_nodes))
    print("\n__________________________")
    for node in caught_nodes:
        print(node['root'].text.decode())
    print("__________________________")
    print("done")

    results = []
    for node in caught_nodes:
        results.append(protego_tree.get_node_by_id(node['root'].id))


    return results
    

if __name__ == "__main__":
    rule = process_rule("test/express/external_resource.yml")
    src_code = read_file("testcode/express/external_resource.js")
    # pre run all the helper patterns
    parsed_src_code = parse_js_code(src_code)
    # create our own tree to be able to make the symbol table and trace the variables
    proTree = ProtegoTree(parsed_src_code)

    caught_nodes = get_matches(proTree, rule)