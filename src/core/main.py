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
        raise Exception("Default rules not implemented yet. Must provide custom rules.")
    
    for target_file in targeted_files:
        for rule in processed_rules:
            scan_file(target_file, rule)
    


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

    src_code = read_file(target_file)
    match_results = get_matches(src_code, processed_rule.patterns, processed_rule.helper_patterns)

    print(f"Match results: {match_results}")
    generate_report(processed_rule, match_results, target_file)
