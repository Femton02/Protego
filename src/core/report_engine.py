import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#

from core.matcher_engine import get_matches
from core.protego_node import ProtegoNode
import json

def generate_report(rule: Rule, match_results: list[ProtegoNode], target_file_path: str, output_format: str = "json") -> None:

    print(f"\nFile: {target_file_path}")
    if len(match_results) == 0:
        print("No vulnerabilities found.")
        return generate_json_report(rule, match_results, target_file_path)
    else:
        print("Vulnerabilities found:")
        print("----------------------------------------------------")
        if output_format == "json":
            json_report = generate_json_report(rule, match_results, target_file_path)
            return json_report
        elif output_format == "html":
            generate_html_report(rule, match_results, target_file_path)
        else:
            generate_text_report(rule, match_results, target_file_path)

def generate_json_report(rule: Rule, match_results: list[ProtegoNode], target_file_path: str) -> None:
    json_report = {
        "rule_id": rule.id,
        "severity": rule.severity,
        "description": rule.description,
        "file_path": target_file_path,
        "detections": []
    }
    for match in match_results:
        detection = {
            "start_line_row": match.start_point[0] + 1,
            "start_line_column": match.start_point[1] + 1,
            "end_line_row": match.end_point[0] + 1,
            "end_line_column": match.end_point[1] + 1,
            "match_content": match.text.decode(),
            "recommendation": rule.message
        }
        json_report["detections"].append(detection)
    return json_report

def generate_html_report(rule: Rule, match_results: list[ProtegoNode], target_file_path: str) -> None:
    pass

def generate_text_report(rule: Rule, match_results: list[ProtegoNode], target_file_path: str) -> None:
    pass

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python report_engine.py <rule_file> <file_path>")
        sys.exit(1)
    rule = process_rule(sys.argv[1])
    src_code = read_file(sys.argv[2])
    match_results = get_matches(src_code, rule.patterns, rule.helper_patterns)
    print(f"Match results: {match_results}")

    generate_report(rule, match_results, sys.argv[2])

    