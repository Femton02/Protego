import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#
#                                   ENTRY POINT
#____________________________________________________________________________________#   

from rule_handler.rule_parser import process_rule
from utils import read_file, get_js_files
from matcher_engine import get_matches
from report_engine import generate_report
from protego_node import ProtegoTree
from symbol_table import SymbolTableBuilder
from matcher_tracer import run_matches


def scan_project(
        project_path: str,
        rule_path: str | None = None,
) -> None:
    """Scans a project for vulnerabilities using custom or default rules.

    Args:
        project_path (str | None, optional): project_path. Defaults to None.
        rule_path (str | None, optional): Path to custom rule. Defaults to None.

    Raises:
        Exception: _description_
    """
    processed_rules = []
    targeted_files = []
    if project_path:
        print(f"Scanning project: {project_path}")
        targeted_files = get_js_files(project_path)
    if rule_path:
        print(f"Rule path: {rule_path}")
        processed_rules.append(process_rule(rule_path))
    else:
        print("No custom rules provided. Using default rules.")
        # TODO: Implement default rules
        for root, dirs, files in os.walk(default_rules_path):
            for file in files:
                if file.endswith(".yml"):
                    processed_rules.append(process_rule(os.path.join(root, file)))
    
    json_report = {}
    for target_file in targeted_files:
        src_code = read_file(target_file)
        parsed_src_code_tree = parse_js_code(src_code)
        protego_tree = ProtegoTree(parsed_src_code_tree)
        json_report[target_file] = {}
        for rule in processed_rules:
            rule_output = scan_file(target_file, rule)
            if len(rule_output["detections"]) > 0:
                json_report[target_file][rule.id] = rule_output
    
    return json_report

def scan_file(
        target_file: str,
        processed_rule: Rule,
) -> None:
    """Scans a file for vulnerabilities based on a rule.

    Args:
        target_file (str): The path to the file to scan.
        processed_rule (Rule): The rule to use for scanning.
    """
    print(f"Scanning file: {target_file} with rule: {processed_rule.id}")
    rule = process_rule("test/express/external_file_upload.yml")
    src_code = read_file("testcode/express/external_file_upload.js")
    # pre run all the helper patterns
    parsed_src_code = parse_js_code(src_code)
    # create our own tree to be able to make the symbol table and trace the variables
    proTree = ProtegoTree(parsed_src_code)

    node_map = proTree.node_mapping
    # create the symbol table
    symbol_table = SymbolTableBuilder()
    symbol_table.build(proTree.root)
    caught_nodes = run_matches(parsed_src_code.root_node, rule.patterns, rule.helper_patterns, proTree)
    result_list = []
    for node in caught_nodes:
        result_list.append(proTree.node_mapping[node['root'].id])
    print(f"Match results: {result_list}")
    report = generate_report(processed_rule, result_list, target_file)
    return report

if __name__ == "__main__":
    scan_project("testcode/express/external_file_upload.js", "test/express/external_file_upload.yml")
    print("done")