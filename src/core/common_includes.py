import os
import sys

workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(workspace_dir)
sys.path.append(os.path.join(workspace_dir, "src"))
sys.path.append(os.path.join(workspace_dir, "src/core"))
sys.path.append(os.path.join(workspace_dir, "src/core/rule_handler"))
sys.path.append(os.path.join(workspace_dir, "src/core/t_sitter"))


from core.rule_handler.rule_parser import process_rule
from core.rule_handler.rule import Rule, Pattern, HelperPattern
from core.t_sitter.tree_sitter_utils import *