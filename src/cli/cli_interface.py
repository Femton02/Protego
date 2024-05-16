import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#


import argparse
from core.main import scan_project

def create_rule(rule_name, rule_description, verbose=False):
    """
    Function to create a new rule.
    Replace this function with actual Protego rule creation logic.
    """
    print(f"Creating rule: {rule_name}")
    print(f"Rule description: {rule_description}")
    if verbose:
        print("Verbose mode enabled. Printing detailed rule creation information.")


class ProtegoCLI:
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(description="CLI for Protego SAST tool")
        self._define_commands()


    def run(self):
        args = self.parser.parse_args()
        if args.command == "scan":
            self._run_scan_command(args)
        elif args.command == "create-rule":
            self._run_create_rule_command(args)
        else:
            self.parser.print_help()
        
    
    def _define_commands(self):
        self.subparsers = self.parser.add_subparsers(title="commands", dest="command", help="Available commands")
        self._define_scan_command()
        self._define_create_rule_command()

    def _define_scan_command(self):
        scan_parser = self.subparsers.add_parser("scan", help="Scan a project", aliases=["s"])

        scan_parser.add_argument("project_path", help="Path to the project to scan")
        scan_parser.add_argument("-r", "--rule-path", help="Path to custom rules")
        scan_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    def _run_scan_command(self, args: argparse.Namespace):
        scan_project(args.project_path, args.rule_path)
    
    def _define_create_rule_command(self):
        create_rule_parser = self.subparsers.add_parser("create-rule", help="Create a new custom rule", aliases=["cr"])

        create_rule_parser.add_argument("rule_name", help="Name of the new rule")
        create_rule_parser.add_argument("rule_directory", help="Location of the new rule")
        create_rule_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    def _run_create_rule_command(self, args):
        create_rule(args.rule_name, args.rule_description, args.verbose)



def main():
    cli = ProtegoCLI()
    cli.run()
    

if __name__ == "__main__":
    main()
