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

def generate_report(rule: Rule, match_results: list[dict], target_file_path: str):
#     {'root': <Node type=object, start_point=(0, 0), end_point=(2, 1)>, 'param1': <Node type=property_identifier, start_point=(1, 0), end_point=(1, 6)>, 'param2': <Node type=object, start_point=(1, 8), end_point=(1, 27)>} for pattern Pattern: javascript_express_cookie_missing_http_only0, {
#   cookie: $<INSECURE_COOKIE>
# }
    print(f"\nFile: {target_file_path}")
    if len(match_results) == 0:
        print("No vulnerabilities found.")
    else:
        print("Vulnerabilities found:")
        for index, match in enumerate(match_results):
            print(f"#{index + 1}:")
            print(f"Rule: {rule.id}")
            print(f"Description: {rule.description}")
            lines = [match["root"].start_point[0] + 1 for match in match_results] 
            print(f"Lines: {lines}")
            print("Match:")
            for key, value in match.items():
                if key == "root":
                    continue
                print(f"{key}: {value.text.decode()}")
            print("\n")
            # print("Recommendation:")
            # print(rule.message)
            # print("\n")
            print("--------------------------------------------")



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

    